from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from .models import UserProfile
from .mailer import send_email
from .authorization import DecisionAuthorization, UserAuthorization
from django.http import Http404
from tastypie import fields
from tastypie.resources import ModelResource, Resource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from imagekit.models import ProcessedImageField


class CommonMeta(object):
    always_return_data = True
    authentication = SessionAuthentication()
    authorization = ReadOnlyAuthorization()


class UserProfileResource(ModelResource):
    class Meta(CommonMeta):
        resource_name = 'smashers'
        queryset = UserProfile.objects.all()
        allowed_methods = ['get']
        fields = ['class_year', 'name', 'major',
                  'id', "has_headshot", "headshot"]
        limit = 20
        test = True

    def dehydrate(self, bundle):
        current_user = bundle.request.user.userprofile
        status = 0
        lookup_id = bundle.data["id"]
        i_like = current_user.people_i_like
        like_me = current_user.people_like_me
        dont_like = current_user.people_i_dont_like

        if i_like.filter(pk=lookup_id).exists():
            status = 1
        if dont_like.filter(pk=lookup_id).exists():
            status = 2
        if (i_like.all() & like_me.all()).filter(pk=lookup_id).exists():
            status = 3
        bundle.data["status"] = status

        return bundle.data

    def obj_get_list(self, bundle, **kwargs):
        # Figure out who I've already rated
        profile = bundle.request.user.userprofile
        like = profile.people_i_like.values_list('pk', flat=True)
        dont_like = profile.people_i_dont_like.values_list('pk', flat=True)
        dont_show = list(like) + list(dont_like)

        # Filter out people I've already rated
        obj_list = super(UserProfileResource, self).obj_get_list(bundle,
                                                                 **kwargs)
        u = obj_list.order_by('?').exclude(pk__in=dont_show)#.filter(lambda profile: hasattr(profile, "user"))
        userfilter = []
        for p in u:
            if p.user:
                userfilter.append(p);
        # print userfilter
        # print type(u)
        return userfilter


class DecisionItem(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}
        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def update(self, other):
        for key in other:
            self.__setattr__(key, other[key])

    def to_dict(self):
        return self._data


class DecisionResource(Resource):
    like = fields.BooleanField(attribute='like')
    user_id = fields.IntegerField(attribute='user_id')
    match = fields.BooleanField(attribute='match')

    class Meta(CommonMeta):
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        object_class = DecisionItem
        resource_name = 'decision'
        authorization = DecisionAuthorization()

    def get_object_list(self, request):
        return []

    def detail_uri_kwargs(self, bundle_or_obj):
        return {}

    def obj_create(self, bundle, **kwargs):
        bundle.obj = DecisionItem(initial=kwargs)
        bundle = self.full_hydrate(bundle)
        rater = bundle.request.user.userprofile
        try:
            ratee = UserProfile.objects.get(pk=bundle.obj.user_id)
        except UserProfile.DoesNotExist:
            raise Http404("Sorry, no user found")

        # Remove the person in case they've already been rated
        rater.people_i_like.remove(ratee)
        rater.people_i_dont_like.remove(ratee)

        if bundle.obj.like:
            rater.people_i_like.add(ratee)
            print "after add"
            match = ratee.people_i_like.filter(pk=rater.pk).exists()
            print "after filter"
            bundle.obj.match = match
            print "after match set"

            if match:
                print "about to notify"
                self._notify_users(rater, ratee)
                print "after notify"

        else:
            rater.people_i_dont_like.add(ratee)
            bundle.obj.match = False

        return bundle

    def _notify_users(self, rater, ratee):
        message = "Hi {}! Looks like {} matched with you. Look each other up!"
        subject = "New JumboSmash Match with {}!"
        print rater.email, ratee.email, subject
        if not settings.DEBUG:
            # send_email([rater.email], subject.format(ratee.name), "Look each other up!")
            # if (rater.email is ratee.email):
                # return
            # send_email([ratee.email], subject.format(rater.name), "Look each other up!")

            send_mail(subject,
                      message.format(rater.name, ratee.name),
                      'jumbosmashers@gmail.com',
                      [rater.email])
            send_mail(subject,
                      message.format(ratee.name, rater.name),
                      'jumbosmashers@gmail.com',
                      [ratee.email])
        print '{} and {} want to smash!'.format(rater.name, ratee.name)


class MatchItem(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}
        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def update(self, other):
        for key in other:
            self.__setattr__(key, other[key])

    def to_dict(self):
        return self._data


class MatchesResource(Resource):
    name = fields.CharField(attribute='name')
    major = fields.CharField(attribute='major')
    class_year = fields.IntegerField(attribute='class_year')
    pk = fields.IntegerField(attribute='pk')
    headshot = fields.FileField(attribute='headshot')

    class Meta(CommonMeta):
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        object_class = MatchItem

    def get_object_list(self, request):
        my_profile = request.user.userprofile
        i_like = my_profile.people_i_like.all()
        like_me = my_profile.people_like_me.all()
        return i_like & like_me

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)


class MultipartResource(object):
    def _fix_body(self, request):
        content_type = request.META.get('CONTENT_TYPE', '')
        is_multipart = content_type.startswith('multipart/form-data')
        if is_multipart and not hasattr(request, '_body'):
            request._body = ''

    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(MultipartResource, self).deserialize(request, data, format)

    def put_detail(self, request, **kwargs):
        self._fix_body(request)
        return super(MultipartResource, self).put_detail(request, **kwargs)

    def put_list(self, request, **kwargs):
        self._fix_body(request)
        return super(MultipartResource, self).put_list(request, **kwargs)

    def patch_detail(self, request, **kwargs):
        self._fix_body(request)
        return super(MultipartResource, self).patch_detail(request, **kwargs)

    def patch_list(self, request, **kwargs):
        self._fix_body(request)
        return super(MultipartResource, self).patch_list(request, **kwargs)


class UserResource(MultipartResource, ModelResource):
    headshot = fields.FileField(attribute='headshot')

    class Meta(CommonMeta):
        queryset = UserProfile.objects.all()
        detail_allowed_methods = ['delete', 'put']
        authorization = UserAuthorization()
        fields = ['headshot', 'id']

    def dispatch(self, request_type, request, **kwargs):
        return super(UserResource, self).dispatch('detail', request, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        kwargs['id'] = bundle.request.user.userprofile.pk
        user = bundle.request.user
        super(UserResource, self).obj_delete(bundle, **kwargs)
        user.delete()

    def obj_update(self, bundle, **kwargs):
        kwargs['id'] = bundle.request.user.userprofile.pk
        retVal = super(UserResource, self).obj_update(bundle, **kwargs)
        bundle.obj.has_headshot = True
        bundle.obj.save()
        return retVal

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        print request.POST
        print request

        data = self.deserialize(request,
                                request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if not user:
            temp_user = User.objects.get(email__iexact=username)
            user = authenticate(username=temp_user.username,
                                password=password)
        if user:
            profile = user.userprofile
            i_like = profile.people_i_like.all()
            like_me = profile.people_like_me.all()
            if user.is_active:
                login(request, user)
                headshot = user.userprofile.headshot
                return self.create_response(request, {
                    'success': True,
                    'user': {
                        "id": user.userprofile.pk,
                        "name": user.userprofile.name,
                        "headshot": headshot.url if headshot else None,
                        "has_headshot": user.userprofile.has_headshot,
                        "num_matches": (i_like & like_me).count()
                    }
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request,
                                        {'success': False},
                                        HttpUnauthorized)

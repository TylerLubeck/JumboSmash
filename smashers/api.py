from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash

from .models import UserProfile
from .authorization import DecisionAuthorization, UserAuthorization
from django.http import Http404
from tastypie import fields
from tastypie.resources import ModelResource, Resource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization


class CommonMeta(object):
    always_return_data = True
    authentication = SessionAuthentication()
    authorization = ReadOnlyAuthorization()


class UserProfileResource(ModelResource):
    class Meta(CommonMeta):
        resource_name = 'smashers'
        queryset = UserProfile.objects.all()
        allowed_methods = ['get']
        fields = ['class_year', 'name', 'major', 'id']
        limit = 20

    def obj_get_list(self, bundle, **kwargs):
        # Figure out who I've already rated
        profile = bundle.request.user.userprofile
        like = profile.people_i_like.values_list('pk', flat=True)
        dont_like = profile.people_i_dont_like.values_list('pk', flat=True)
        dont_show = list(like) + list(dont_like)

        # Filter out people I've already rated
        obj_list = super(UserProfileResource, self).obj_get_list(bundle,
                                                                 **kwargs)
        return obj_list.order_by('?').exclude(pk__in=dont_show)


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
            match = ratee.people_i_like.filter(pk=rater.pk).exists()
            bundle.obj.match = match

            if match:
                self._notify_users(rater, ratee)
            else:
                rater.people_i_dont_like.add(ratee)
                bundle.obj.match = False

        return bundle

    def _notify_users(self, rater, ratee):
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

    class Meta(CommonMeta):
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        object_class = MatchItem

    def get_object_list(self, request):
        my_profile = request.user.userprofile
        i_like = my_profile.people_i_like.all()
        like_me = my_profile.people_like_me.all()
        print i_like & like_me
        return i_like & like_me

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)


class MultipartResource(object):
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


class UserResource(MultipartResource, ModelResource):
    headshot = fields.FileField(attribute='headshot')
    class Meta:
        queryset = UserProfile.objects.all()
        detail_allowed_methods = ['delete', 'post']
        # authorization = UserAuthorization() #TODO: PUT THIS BACK
        fields = ['headshot']

    def obj_delete(self, bundle, **kwargs):
        user = bundle.request.user
        super(UserResource, self).obj_delete(bundle, **kwargs)
        user.delete()

    def obj_create(self, bundle, **kwargs):
        print 'CREATING USER HEADSHOT'
        print kwargs
        return super(UserResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, **kwargs):
        print 'GOT EM'
        return super(UserResource, self).obj_update(bundle, **kwargs)

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
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)

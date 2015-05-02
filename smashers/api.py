from .models import UserProfile
from .authorization import DecisionAuthorization
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

    def get_object_list(self, request):
        # Figure out who I've already rated
        profile = request.user.userprofile
        like = profile.people_i_like.values_list('pk', flat=True)
        dont_like = profile.people_i_dont_like.values_list('pk', flat=True)
        dont_show = list(like) + list(dont_like)

        # Filter out people I've already rated
        qs = super(UserProfileResource, self).get_object_list(request)
        qs = qs.order_by('?').exclude(pk__in=dont_show)
        return qs

    def prepend_urls(self):
        # TODO: STUB
        return super(UserProfileResource, self).prepend_urls()


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
        raterprofile = bundle.request.user.userprofile
        try:
            rated_person = UserProfile.objects.get(pk=bundle.obj.user_id)
        except UserProfile.DoesNotExist:
            # TODO: Throw a 404
            raise
        if bundle.obj.like:
            raterprofile.people_i_like.add(rated_person)
            match = rated_person.people_i_like.filter(pk=raterprofile.pk).exists()
            bundle.obj.match = match
        else:
            raterprofile.people_i_dont_like.add(rated_person)
            bundle.obj.match = False

        return bundle


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
    class Meta(CommonMeta):
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        object_class = MatchItem

    def _get_matches(self, my_id, my_likes):
        matches = []
        for person in my_likes:
            if person.people_i_like.filter(pk=my_id).exists():
                matches.append(person)
        return matches

    def get_object_list(self, request):
        my_profile = request.user.userprofile
        my_likes = my_profile.people_i_like.all()
        matches = self._get_matches(my_profile.pk, my_likes)
        print matches
        return matches

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)


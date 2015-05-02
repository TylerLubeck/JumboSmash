from .models import UserProfile
from tastypie.resources import ModelResource

class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()

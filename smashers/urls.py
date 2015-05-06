from django.conf.urls import include, url
from tastypie.api import Api
from .api import (UserProfileResource, DecisionResource,
                  MatchesResource, UserResource)
import views

v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(DecisionResource())
v1_api.register(MatchesResource())
v1_api.register(UserResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^accounts/register/$',
        views.SmasherRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^image_upload/$',
    #     views.UploadImageView.as_view(),
    #     name='image_upload'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dev/', views.TestView.as_view(), name='genderize')
]

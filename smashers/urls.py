from django.conf.urls import include, url
from tastypie.api import Api
from .api import UserProfileResource, DecisionResource, MatchesResource
import views

v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(DecisionResource())
v1_api.register(MatchesResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^accounts/register/$',
        views.SmasherRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
]

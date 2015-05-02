from django.conf.urls import include, url
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'users', views.UserProfileViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^accounts/register/$',
        views.SmasherRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
]

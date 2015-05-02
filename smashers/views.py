from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from registration.signals import user_activated
from registration.backends.default.views import RegistrationView
from rest_framework import viewsets
from .forms import SmasherRegistrationForm
from .models import UserProfile
from .serializers import UserProfileSerializer


def associate_profile(sender, user, request, **kwargs):
    email = user.email
    # If this function gets called, then the userprofile must exist
    up = UserProfile.objects.get(email__iexact=email)
    up.user = user
    up.save()

user_activated.connect(associate_profile)


class SmasherRegistrationView(RegistrationView):
    form_class = SmasherRegistrationForm


class IndexView(View):
    def get(self, request):
        return render(request, 'smashers/index.html')


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

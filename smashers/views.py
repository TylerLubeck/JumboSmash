from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from registration.signals import user_activated
from registration.backends.default.views import RegistrationView
from .forms import SmasherRegistrationForm, ImageUploadForm
from .models import UserProfile
import json


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
        # TODO: Put this code in a Cache block
        # TODO: Add template variable on if they have an image or not
        people = UserProfile.objects.values('name', 'pk', 'major')
        for p in people:
            p['tokens'] = [p['name'], p['major']]
        serialized_names = json.dumps(list(people))
        context = {
            'people': serialized_names,
            'has_image': True # TODO: Compute this
        }
        return render(request, 'smashers/index.html', context)


from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from registration.signals import user_activated
from registration.backends.default.views import RegistrationView
from .forms import SmasherRegistrationForm, ImageUploadForm
from django.contrib.auth.models import User
from .models import UserProfile
import json
import urllib, urllib2


def associate_profile(sender, user, request, **kwargs):
    email = user.email
    # If this function gets called, then the userprofile must exist
    up = UserProfile.objects.get(email__iexact=email)
    up.user = user
    up.save()

user_activated.connect(associate_profile)

class SmasherRegistrationView(RegistrationView):
    form_class = SmasherRegistrationForm
    success_url = '/?reg=true'


class TestView(View):
    def get(self, request):
        if not request.user.is_superuser:
            print "Not for u"
            return render(request, 'registration/login.html')


        # # url = 'http://api.genderize.io/?name='
        users = list(User.objects.all())
        for user in users:
            if user and user.is_active is False and user.email is not None and not hasattr(user, "userprofile"):
                profile = UserProfile.objects.filter(email__iexact=user.email);
                if len(profile) > 0:
                    profile = profile[0];
                    user.is_active = True;
                    user.userprofile = profile
                    profile.user_id = user.id;
                    profile.save()
                    user.save();

        # for profile in users:
        #     arr = profile.name.split(" ")
        #     if arr:
        #         firstname = arr[0];
        #         req = urllib2.Request(url + firstname)
        #         req.add_header("Accept-Language", "en-US")
        #         req.add_header("Accept-Encoding", "gzip")
        #         req.add_header("Connection", "Keep-Alive")
        #         req.add_header("Content-Type", "application/x-www-form-urlencoded")
        #         res = urllib2.urlopen(req)
        #         blob = json.loads(res.read());
        #         print blob
        #         print blob.get("gender")
        #         print blob.get("count")
        #         # gender = blob.get("gender", None) if int(blob.get("probabality", 0)) > .95 else None;
        #         # print gender

        return render(request, 'registration/login.html')

class IndexView(View):
    def get(self, request):
        # TODO: Put this code in a Cache block
        # TODO: Add template variable on if they have an image or not
        # up = UserProfile.objects.get(email__iexact=email)
        user = request.user
        user_info = {"error": "Not authenticated", "is_authenticated": False}

        if not user.is_anonymous() and user.is_authenticated():
            profile = user.userprofile
            i_like = profile.people_i_like.all()
            like_me = profile.people_like_me.all()
            print i_like
            print like_me

            user_info = {
                "id": profile.pk,
                "is_authenticated": True,
                "name": profile.name,
                "has_headshot": profile.has_headshot,
                "headshot": profile.headshot.url if profile.headshot else None,
                "num_matches": (i_like & like_me).count()
            }


        people = UserProfile.objects.values('name', 'pk', 'major')
        for p in people:
            p['tokens'] = [p['name'], p['major']]
        serialized_names = json.dumps(list(people))
        context = {
            'people': serialized_names,
            'user': json.dumps(user_info),
            'is_authenticated': user.is_authenticated()
        }
        return render(request, 'smashers/index.html', context)

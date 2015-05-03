from registration.forms import RegistrationFormUniqueEmail
from django import forms
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
from .models import UserProfile


class SmasherRegistrationForm(RegistrationFormUniqueEmail):
    def clean_email(self):
        email = super(SmasherRegistrationForm, self).clean_email()
        # If the user trying to register doesn't exist in our database,
        # then don't let them register.
        try:
            UserProfile.objects.get(email__iexact=email)
            return email
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("We don't have you in our database")

class ImageUploadForm(forms.Form):
    # headshot = ProcessedImageField(spec_id='headshot_form',
    #                                processors=[ResizeToFill(300, 300)],
    #                                null=True,
    #                                blank=True)

    headshot = forms.ImageField()

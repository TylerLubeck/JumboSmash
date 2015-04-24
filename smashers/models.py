from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    major = models.CharField(max_length=200,
                             help_text='The Person\'s major')

    name = models.CharField(max_length=200,
                            help_text='The Person\'s name')

    class_year = models.IntegerField(help_text='The graduation year')

    email = models.EmailField(help_text='The user\'s Tufts Email')

    user = models.OneToOneField(User, null=True, blank=True)

    people_i_like = models.ManyToManyField('self',
                                           symmetrical=False,
                                           related_name='people_like_me')

    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        is_registered = self.user is not None
        return '{} - Registered: {}'.format(self.name,
                                            'Yes' if is_registered else 'No')

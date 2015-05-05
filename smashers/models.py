from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



class UserProfile(models.Model):
    major = models.CharField(max_length=200,
                             help_text='The Person\'s major')

    name = models.CharField(max_length=200,
                            help_text='The Person\'s name')

    class_year = models.IntegerField(help_text='The graduation year')

    email = models.EmailField(help_text='The user\'s Tufts Email')

    user = models.OneToOneField(User, null=True, blank=True)

    headshot = ProcessedImageField(upload_to='headshots',
                                   processors=[ResizeToFill(300, 300)],
                                   null=True,
                                   blank=True)

    # headshot = models.ImageField(upload_to='headshots',
    #                              null=True,
    #                              blank=True)

    has_headshot = models.BooleanField(default=False)



    people_i_like = models.ManyToManyField('self',
                                           symmetrical=False,
                                           related_name='people_like_me',
                                           blank=True)

    people_i_dont_like = models.ManyToManyField('self',
                                                symmetrical=False,
                                                related_name='people_dont_like_me',
                                                blank=True)


    def is_registered(self):
        return self.user != None
    is_registered.short_description = 'Registered'
    is_registered.boolean = True
    def __str__(self):
        return self.name

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('major', models.CharField(help_text=b"The Person's major", max_length=200)),
                ('name', models.CharField(help_text=b"The Person's name", max_length=200)),
                ('class_year', models.IntegerField(help_text=b'The graduation year')),
                ('email', models.EmailField(help_text=b"The user's Tufts Email", max_length=254)),
                ('headshot', imagekit.models.fields.ProcessedImageField(null=True, upload_to=b'headshots', blank=True)),
                ('has_headshot', models.BooleanField(default=False)),
                ('people_i_dont_like', models.ManyToManyField(related_name='people_dont_like_me', to='smashers.UserProfile', blank=True)),
                ('people_i_like', models.ManyToManyField(related_name='people_like_me', to='smashers.UserProfile', blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

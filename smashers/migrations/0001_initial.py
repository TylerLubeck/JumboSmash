# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('people_i_like', models.ManyToManyField(to='smashers.UserProfile')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

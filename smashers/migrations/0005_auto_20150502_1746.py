# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smashers', '0004_userprofile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='people_i_dont_like',
            field=models.ManyToManyField(related_name='people_dont_like_me', to='smashers.UserProfile'),
        ),
    ]

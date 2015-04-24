# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smashers', '0002_auto_20150416_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='people_i_like',
            field=models.ManyToManyField(related_name='people_like_me', to='smashers.UserProfile'),
        ),
    ]

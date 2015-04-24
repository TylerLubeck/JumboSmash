# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smashers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='people_i_like',
            field=models.ManyToManyField(related_name='gonna_smash', to='smashers.UserProfile'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-03 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_profile_registration_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
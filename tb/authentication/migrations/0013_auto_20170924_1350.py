# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-24 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_auto_20170915_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='emailnotify',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='smsnotify',
            field=models.BooleanField(default=True),
        ),
    ]

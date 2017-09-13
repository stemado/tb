# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-11 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_profile_pharmacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('0', 'Administrator'), ('1', 'Patient')], default='Patient', max_length=20),
        ),
    ]
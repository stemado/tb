# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-26 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_auto_20170924_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tandc',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('0', 'Administrator'), ('1', 'Patient')], default='1', max_length=20),
        ),
    ]

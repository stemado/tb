# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-26 19:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20170826_1431'),
    ]

    operations = [
        migrations.RenameField(
            model_name='individualuser',
            old_name='address1',
            new_name='individualTest',
        ),
        migrations.RemoveField(
            model_name='individualuser',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='individualuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='individualuser',
            name='mobilenumber',
        ),
        migrations.RemoveField(
            model_name='individualuser',
            name='phonenumber',
        ),
        migrations.RemoveField(
            model_name='individualuser',
            name='providence',
        ),
        migrations.RemoveField(
            model_name='individualuser',
            name='zipcode',
        ),
    ]

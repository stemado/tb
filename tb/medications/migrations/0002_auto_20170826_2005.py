# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-27 01:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medication',
            old_name='medicationPatient',
            new_name='user',
        ),
    ]

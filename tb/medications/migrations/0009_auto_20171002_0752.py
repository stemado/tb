# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-02 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0008_auto_20171002_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicationcompletion',
            name='completionEdited',
            field=models.BooleanField(default=False, max_length=50, verbose_name='Medicaton Edited'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-18 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0005_auto_20170915_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicationcompletion',
            name='completionStatus2',
            field=models.CharField(blank=True, choices=[('Null', 'Null'), ('False', 'False'), ('True', 'True')], default='Null', max_length=12, null=True, verbose_name='Current Status 2'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-02 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0011_remove_medicationcompletion_completionedited'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicationcompletion',
            name='completionEdited',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Medicaton Edited'),
        ),
        migrations.AlterField(
            model_name='medicationcompletion',
            name='completionEditedDate',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Date by:'),
        ),
    ]

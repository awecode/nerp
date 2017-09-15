# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0020_auto_20170214_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporttable',
            name='title_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reporttable',
            name='title_ne',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reporttabledetail',
            name='field_name_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='reporttabledetail',
            name='field_name_ne',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

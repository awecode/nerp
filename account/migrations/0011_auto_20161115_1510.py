# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-15 09:25
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20161018_1209'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]

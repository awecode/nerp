# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-02 08:37
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0003_auto_20160630_1205'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='targetgroup',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]

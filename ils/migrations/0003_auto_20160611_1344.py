# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-11 07:59
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0002_auto_20160528_1957'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='subject',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
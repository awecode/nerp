# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-28 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0027_auto_20170227_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='insurance_id_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
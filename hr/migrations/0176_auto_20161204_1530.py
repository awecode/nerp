# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-04 09:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0175_auto_20161204_1148'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaxCalcScheme',
            new_name='IncomeTaxCalcScheme',
        ),
        migrations.RenameModel(
            old_name='TaxScheme',
            new_name='IncomeTaxScheme',
        ),
    ]

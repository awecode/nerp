# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-31 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0014_employee_code_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeefacility',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employeefacility',
            name='name_ne',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
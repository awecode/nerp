# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0010_auto_20170808_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenditureHead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=20, verbose_name='Expenditure Head Number')),
                ('name', models.CharField(max_length=20, verbose_name='Expenditure Head Name')),
            ],
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='expenditure_head_name',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='expenditure_head_name_en',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='expenditure_head_name_ne',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='expenditure_head_number',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='expenditure_head_number_en',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='expenditure_head_number_ne',
        ),
    ]

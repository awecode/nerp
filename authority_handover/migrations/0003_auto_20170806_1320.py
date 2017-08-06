# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0002_auto_20170804_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorityhandover',
            name='beneficiary_designation_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='authorityhandover',
            name='beneficiary_designation_ne',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='authorityhandover',
            name='beneficiary_office_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='authorityhandover',
            name='beneficiary_office_ne',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='budgetdistribution',
            name='expenditure_head_name_en',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='budgetdistribution',
            name='expenditure_head_name_ne',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='budgetdistribution',
            name='expenditure_head_number_en',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='budgetdistribution',
            name='expenditure_head_number_ne',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

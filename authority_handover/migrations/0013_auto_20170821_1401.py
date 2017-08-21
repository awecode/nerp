# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0012_budgetdistribution_expenditure_head'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditurehead',
            name='name_en',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Name'),
        ),
        migrations.AddField(
            model_name='expenditurehead',
            name='name_ne',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Name'),
        ),
        migrations.AddField(
            model_name='expenditurehead',
            name='number_en',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Number'),
        ),
        migrations.AddField(
            model_name='expenditurehead',
            name='number_ne',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Number'),
        ),
    ]

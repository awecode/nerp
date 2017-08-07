# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0005_remove_budgetdistribution_foreign_fund_loan_commodity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=255, verbose_name='Beneficiary Designation')),
                ('designation_en', models.CharField(max_length=255, null=True, verbose_name='Beneficiary Designation')),
                ('designation_ne', models.CharField(max_length=255, null=True, verbose_name='Beneficiary Designation')),
                ('office', models.CharField(max_length=255, verbose_name='Beneficiary Office')),
                ('office_en', models.CharField(max_length=255, null=True, verbose_name='Beneficiary Office')),
                ('office_ne', models.CharField(max_length=255, null=True, verbose_name='Beneficiary Office')),
            ],
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='beneficiary_designation',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='beneficiary_designation_en',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='beneficiary_designation_ne',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='beneficiary_office',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='beneficiary_office_en',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='beneficiary_office_ne',
        ),
        migrations.AddField(
            model_name='authorityhandover',
            name='beneficiary',
            field=models.ForeignKey(related_name='authority_handovers', verbose_name='Beneficiary', blank=True, to='authority_handover.Beneficiary', null=True),
        ),
    ]

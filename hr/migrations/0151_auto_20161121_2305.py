# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-21 17:20
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20161115_1510'),
        ('hr', '0150_auto_20161121_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollconfig',
            name='allowance_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_allowance', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='basic_salary_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_basic_salary', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='deduction_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_deduction', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='incentive_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_incentive', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='pay_head_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_pay_head', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='pro_tempore_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_pro_tempore', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='salary_giving_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_salary_giving', to='account.Category'),
        ),
        migrations.AddField(
            model_name='payrollconfig',
            name='tax_account_category',
            field=mptt.fields.TreeOneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='config_tax', to='account.Category'),
        ),
    ]

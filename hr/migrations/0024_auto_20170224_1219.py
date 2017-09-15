# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-24 06:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0023_bankbranch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Employee'},
        ),
        migrations.AddField(
            model_name='employee',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='hr.Bank'),
        ),
        migrations.AddField(
            model_name='employee',
            name='bank_account_number',
            field=models.CharField(default='11111111', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='bank_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='hr.BankBranch'),
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together=set([('bank', 'bank_branch', 'bank_account_number')]),
        ),
    ]
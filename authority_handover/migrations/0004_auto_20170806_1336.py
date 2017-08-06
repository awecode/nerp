# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0003_auto_20170806_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorityhandover',
            name='beneficiary_designation',
            field=models.CharField(max_length=255, verbose_name='Beneficiary Designation'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='beneficiary_designation_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Beneficiary Designation'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='beneficiary_designation_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Beneficiary Designation'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='beneficiary_office',
            field=models.CharField(max_length=255, verbose_name='Beneficiary Office'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='beneficiary_office_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Beneficiary Office'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='beneficiary_office_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Beneficiary Office'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='budget_head',
            field=models.ForeignKey(related_name='authority_handovers', verbose_name='Budget Head', to='core.BudgetHead'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='fiscal_year',
            field=models.ForeignKey(related_name='authority_handovers', verbose_name='Fiscal Year', to='core.FiscalYear'),
        ),
        migrations.AlterField(
            model_name='authorityhandover',
            name='priority_code',
            field=models.CharField(max_length=10, verbose_name='Priority Code'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='donor',
            field=models.ForeignKey(verbose_name='Donor', to='core.Donor'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='expenditure_head_name',
            field=models.CharField(max_length=20, verbose_name='Expenditure Head Name'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='expenditure_head_name_en',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Name'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='expenditure_head_name_ne',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Name'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='expenditure_head_number',
            field=models.CharField(max_length=20, verbose_name='Expenditure Head Number'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='expenditure_head_number_en',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Number'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='expenditure_head_number_ne',
            field=models.CharField(max_length=20, null=True, verbose_name='Expenditure Head Number'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_cash',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Grant Cash'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_commodity',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Grant Commodity'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_direct_payment',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Grant Direct Payment'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_reimbursable',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Grant Reimbursable'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_cash',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Loan Cash'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_commodity',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Loan Commodity'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_direct_payment',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Loan Direct Payment'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_reimbursable',
            field=models.PositiveIntegerField(verbose_name='Foreign Fund Loan Reimbursable'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='government_fund',
            field=models.PositiveIntegerField(verbose_name='Government Fund'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='permitted_budget',
            field=models.PositiveIntegerField(verbose_name='Permitted Budget'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='remarks',
            field=models.CharField(max_length=255, verbose_name='Remarks'),
        ),
    ]

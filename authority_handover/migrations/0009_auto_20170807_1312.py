# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0008_auto_20170807_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_cash',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Grant Cash'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_commodity',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Grant Commodity'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_direct_payment',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Grant Direct Payment'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_reimbursable',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Grant Reimbursable'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_cash',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Loan Cash'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_direct_payment',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Loan Direct Payment'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_reimbursable',
            field=models.PositiveIntegerField(default=0, verbose_name='Foreign Fund Loan Reimbursable'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='government_fund',
            field=models.PositiveIntegerField(default=0, verbose_name='Government Fund'),
        ),
        migrations.AlterField(
            model_name='budgetdistribution',
            name='permitted_budget',
            field=models.PositiveIntegerField(default=0, verbose_name='Permitted Budget'),
        ),
    ]

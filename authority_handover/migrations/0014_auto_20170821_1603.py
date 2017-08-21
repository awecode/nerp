# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_budgethead_recurrent'),
        ('authority_handover', '0013_auto_20170821_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignFund',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(verbose_name='Amount')),
                ('type', models.CharField(max_length=5, verbose_name='Type', choices=[(b'grant', b'Grant'), (b'loan', b'Loan')])),
                ('sub_type', models.CharField(max_length=15, verbose_name='Sub Type', choices=[(b'cash', b'Cash'), (b'reimbursable', b'Reimbursable'), (b'direct payment', b'Direct Payment'), (b'commodity', b'Commodity')])),
            ],
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='donor',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_cash',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_commodity',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_direct_payment',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_grant_reimbursable',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_cash',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_direct_payment',
        ),
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_reimbursable',
        ),
        migrations.AddField(
            model_name='foreignfund',
            name='budget_distribution',
            field=models.ForeignKey(related_name='foreign_funds', verbose_name='Budget Distribution', to='authority_handover.BudgetDistribution'),
        ),
        migrations.AddField(
            model_name='foreignfund',
            name='donor',
            field=models.ForeignKey(related_name='foreign_funds', verbose_name='Donor', to='core.Donor'),
        ),
    ]

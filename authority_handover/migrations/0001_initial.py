# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_budgethead_recurrent'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorityHandover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficiary_designation', models.CharField(max_length=255)),
                ('beneficiary_office', models.CharField(max_length=255)),
                ('priority_code', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('budget_head', models.ForeignKey(related_name='authority_handovers', to='core.BudgetHead')),
                ('fiscal_year', models.ForeignKey(related_name='authority_handovers', to='core.FiscalYear')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='authority_handover.AuthorityHandover', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BudgetDistribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expenditure_head_number', models.CharField(max_length=20)),
                ('expenditure_head_name', models.CharField(max_length=20)),
                ('permitted_budget', models.PositiveIntegerField()),
                ('government_fund', models.PositiveIntegerField()),
                ('foreign_fund_grant_cash', models.PositiveIntegerField()),
                ('foreign_fund_grant_reimbursable', models.PositiveIntegerField()),
                ('foreign_fund_grant_direct_payment', models.PositiveIntegerField()),
                ('foreign_fund_grant_commodity', models.PositiveIntegerField()),
                ('foreign_fund_loan_cash', models.PositiveIntegerField()),
                ('foreign_fund_loan_reimbursable', models.PositiveIntegerField()),
                ('foreign_fund_loan_direct_payment', models.PositiveIntegerField()),
                ('foreign_fund_loan_commodity', models.PositiveIntegerField()),
                ('remarks', models.CharField(max_length=255)),
                ('authority_handover', models.ForeignKey(related_name='budget_distributions', to='authority_handover.AuthorityHandover')),
                ('donor', models.ForeignKey(to='core.Donor')),
            ],
        ),
    ]

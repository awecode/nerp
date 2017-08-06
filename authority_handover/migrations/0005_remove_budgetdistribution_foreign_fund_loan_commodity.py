# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0004_auto_20170806_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetdistribution',
            name='foreign_fund_loan_commodity',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0011_auto_20170821_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetdistribution',
            name='expenditure_head',
            field=models.ForeignKey(related_name='budget_distributions', blank=True, to='authority_handover.ExpenditureHead', null=True),
        ),
    ]

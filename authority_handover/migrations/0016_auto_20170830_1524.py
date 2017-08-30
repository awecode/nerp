# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0015_auto_20170823_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficiary',
            name='designation_en',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='designation_ne',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='office',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='office_en',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='office_ne',
        ),
    ]

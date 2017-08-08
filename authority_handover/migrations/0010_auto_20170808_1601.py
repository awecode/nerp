# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0009_auto_20170807_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorityhandover',
            name='date',
            field=njango.fields.BSDateField(verbose_name='Date'),
        ),
    ]

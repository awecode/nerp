# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0006_auto_20170807_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beneficiary',
            options={'verbose_name_plural': 'Beneficiaries'},
        ),
    ]

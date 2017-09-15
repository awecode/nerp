# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_data_store'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockentry',
            options={'verbose_name_plural': 'Stock Entries'},
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfy',
            name='additional_advances',
            field=models.ForeignKey(related_name='additional_advances_for', default=1, to='account.Account'),
            preserve_default=False,
        ),
    ]

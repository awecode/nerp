# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteminstance',
            name='source',
            field=models.ForeignKey(blank=True, to='inventory.EntryReportRow', null=True),
        ),
    ]

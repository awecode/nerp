# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20150525_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=njango.fields.BSDateField(),
        ),
    ]

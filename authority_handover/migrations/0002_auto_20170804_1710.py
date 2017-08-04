# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorityhandover',
            name='level',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='authorityhandover',
            name='tree_id',
        ),
    ]

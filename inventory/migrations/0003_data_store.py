# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def item_location(apps, schema_editor):
    from inventory.models import ItemLocation

    ItemLocation.objects.create(name='Store')


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0002_auto_20160528_1957'),
    ]

    operations = [
        migrations.RunPython(item_location),
    ]

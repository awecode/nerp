# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db.models.signals import post_save



def fiscal_years(apps, schema_editor):
    from core.models import FiscalYear
    # FiscalYear = apps.get_model('core', 'FiscalYear')
    post_save.disconnect(sender=FiscalYear)
    FiscalYear.objects.get_or_create(year=2069)
    FiscalYear.objects.get_or_create(year=2070)
    FiscalYear.objects.get_or_create(year=2071)
    FiscalYear.objects.get_or_create(year=2072)
    FiscalYear.objects.get_or_create(year=2073)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fiscal_years),
    ]

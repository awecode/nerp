# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0007_auto_20170807_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='designation',
            field=models.CharField(max_length=255, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='designation_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='designation_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='office',
            field=models.CharField(max_length=255, verbose_name='Office'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='office_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Office'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='office_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Office'),
        ),
    ]

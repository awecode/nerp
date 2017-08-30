# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0016_auto_20170830_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='designation_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Designation'),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='designation_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Designation'),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='office',
            field=models.ForeignKey(verbose_name='Office', blank=True, to='authority_handover.Office', null=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='office_en',
            field=models.ForeignKey(verbose_name='Office', blank=True, to='authority_handover.Office', null=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='office_ne',
            field=models.ForeignKey(verbose_name='Office', blank=True, to='authority_handover.Office', null=True),
        ),
    ]

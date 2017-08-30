# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0017_auto_20170830_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='office',
            field=models.ForeignKey(default=1, verbose_name='Office', to='authority_handover.Office'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='office_en',
            field=models.ForeignKey(verbose_name='Office', to='authority_handover.Office', null=True),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='office_ne',
            field=models.ForeignKey(verbose_name='Office', to='authority_handover.Office', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-11 07:59
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.deletion
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisbursementDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wa_no', models.PositiveIntegerField(blank=True, null=True)),
                ('requested_date', njango.fields.BSDateField(blank=True, default=njango.fields.today, null=True, validators=[core.models.validate_in_fy])),
                ('disbursement_method', models.CharField(choices=[(b'reimbursement', b'Reimbursement'), (b'replenishment', b'Replenishment'), (b'liquidation', b'Liquidation'), (b'direct_payment', b'Direct Payment')], max_length=255)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('aid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Aid')),
                ('project_fy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ProjectFy')),
            ],
        ),
    ]

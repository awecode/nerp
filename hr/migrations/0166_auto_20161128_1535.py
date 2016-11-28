# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-28 09:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0165_auto_20161128_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProTemporeDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('pro_tempore', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pro_tempore_record', to='hr.ProTempore')),
            ],
        ),
        migrations.RemoveField(
            model_name='paymentrecord',
            name='pro_tempore_amount',
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='pro_tempore_details',
            field=models.ManyToManyField(blank=True, to='hr.ProTemporeDetail'),
        ),
    ]

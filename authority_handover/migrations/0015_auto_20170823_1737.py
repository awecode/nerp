# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority_handover', '0014_auto_20170821_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('district', models.ForeignKey(verbose_name='District', to='authority_handover.District')),
            ],
        ),
        migrations.AddField(
            model_name='authorityhandover',
            name='parent',
            field=models.OneToOneField(related_name='child', null=True, blank=True, to='authority_handover.AuthorityHandover'),
        ),
        migrations.AddField(
            model_name='authorityhandover',
            name='type',
            field=models.CharField(default='first', max_length=15, choices=[(b'first', 'First'), (b'addition', 'Addition'), (b'edited', 'Edited')]),
            preserve_default=False,
        ),
    ]

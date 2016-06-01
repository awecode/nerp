# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hr.models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0104_auto_20160527_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeaccount',
            name='account',
            field=models.OneToOneField(related_name='employee_account', validators=[hr.models.employee_account_validator], to='account.Account'),
        ),
    ]

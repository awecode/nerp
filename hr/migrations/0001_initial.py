# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_holder_type', models.CharField(max_length=50, choices=[(b'EMPLOYEE', "Employee's Account"), (b'COMPANY', 'Company Account')])),
                ('account_type', models.CharField(max_length=50, choices=[(b'BANK ACC', 'Bank Account'), (b'INSURANCE ACC', 'InsuranceAccount'), (b'NALA ACC', 'Nagarik Lagani Kosh Account'), (b'SANCHAI KOSH', 'Sanchai Kosh')])),
                ('org_name', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=150)),
                ('acc_number', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Allowence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('amount_rate', models.FloatField(null=True, blank=True)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='BranchOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('amount_rate', models.FloatField(null=True, blank=True)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('budget_code', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=1, choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('pan_number', models.CharField(max_length=100)),
                ('payment_halt', models.BooleanField(default=False)),
                ('appoint_date', models.DateField(auto_now_add=True)),
                ('dismiss_date', models.DateField(null=True, blank=True)),
                ('is_permanent', models.BooleanField(default=False)),
                ('allowence', models.ManyToManyField(to='hr.Allowence', blank=True)),
                ('bank_account', models.OneToOneField(related_name='bank_account', to='hr.Account')),
                ('designation', models.ForeignKey(to='hr.Designation')),
                ('employee', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade_name', models.CharField(max_length=100)),
                ('salary_scale', models.FloatField()),
                ('grade_number', models.PositiveIntegerField()),
                ('grade_rate', models.FloatField()),
                ('is_technical', models.BooleanField(default=False)),
                ('parent_grade', models.ForeignKey(blank=True, to='hr.EmployeeGrade', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incentive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('amount_rate', models.FloatField(null=True, blank=True)),
                ('description', models.CharField(max_length=250)),
                ('employee_grade', models.ForeignKey(to='hr.EmployeeGrade')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeTaxRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_from', models.FloatField()),
                ('end_to', models.FloatField()),
                ('tax_rate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payed_from_date', models.DateField()),
                ('payed_to_date', models.DateField()),
                ('absent_days', models.PositiveIntegerField()),
                ('allowence', models.FloatField(null=True, blank=True)),
                ('incentive', models.FloatField(null=True, blank=True)),
                ('payed_amout', models.FloatField()),
                ('deduction', models.ManyToManyField(to='hr.Deduction')),
                ('payed_employee', models.ForeignKey(to='hr.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='PayrollEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('entry_row', models.ManyToManyField(to='hr.PaymentRecord')),
            ],
        ),
        migrations.CreateModel(
            name='ProTempore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appoint_date', models.DateField(auto_now_add=True)),
                ('dismiss_date', models.DateField(null=True, blank=True)),
                ('employee', models.OneToOneField(related_name='real_employee_post', to='hr.Employee')),
                ('pro_tempore', models.OneToOneField(related_name='virtual_employee_post', to='hr.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit', models.FloatField()),
                ('debit', models.FloatField()),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(to='hr.Account')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='incentive',
            field=models.ManyToManyField(to='hr.Incentive', blank=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='insurance_account',
            field=models.OneToOneField(related_name='insurance_acc', to='hr.Account'),
        ),
        migrations.AddField(
            model_name='employee',
            name='nalakosh_account',
            field=models.OneToOneField(related_name='nalakosh_acc', to='hr.Account'),
        ),
        migrations.AddField(
            model_name='employee',
            name='sanchai_account',
            field=models.OneToOneField(related_name='sanchai_acc', to='hr.Account'),
        ),
        migrations.AddField(
            model_name='employee',
            name='working_branch',
            field=models.ForeignKey(to='hr.BranchOffice'),
        ),
        migrations.AddField(
            model_name='designation',
            name='grade',
            field=models.ForeignKey(to='hr.EmployeeGrade'),
        ),
        migrations.AddField(
            model_name='allowence',
            name='employee_grade',
            field=models.ForeignKey(to='hr.EmployeeGrade'),
        ),
    ]
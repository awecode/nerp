# import dbsettings
import math
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from mptt.fields import TreeForeignKey, TreeOneToOneField
from mptt.models import MPTTModel
from solo.models import SingletonModel

from app.settings import BASE_DIR
from core.models import FiscalYear
from hr.fields import HRBSDateField, today
from users.models import User
# from core.models import validate_in_fy
# from .fields import HRBSDateField, today
from njango.nepdate import bs2ad, bs
from django.core.validators import MaxValueValidator, MinValueValidator
from calendar import monthrange as mr
from datetime import date
from hr.bsdate import BSDate
from .helpers import get_y_m_tuple_list, are_side_months, get_validity_slots, get_validity_id, \
    employee_last_payment_record, drc_1_day, get_y_m_in_words
from django.core.exceptions import ValidationError
# import pdb

from django.dispatch.dispatcher import receiver

from account.models import Account, Category
from django.db.models.signals import post_save, post_delete, m2m_changed

from jsonfield import JSONField

import copy

deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]

payment_cycle = [('M', _('Monthly')),
                 ('Y', _('Yearly')),
                 ('D', _('Daily')),
                 ]


# Accout Category settingShoul

# Account Category
#  >> Pay Head
#    >> Basic Salary
#    >> Deduction
#    >> Allowance
#    >> Incentive
#    >> Tax
#    >> Pro Tempore
#  >> Salary Giving


class Bank(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class BankBranch(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class EmployeeGradeGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


# FIXME valid from from be greter than previous and less than now date(serializer level validation done)
class GradeScaleValidity(models.Model):
    valid_from = HRBSDateField()
    note = models.CharField(max_length=150)

    def __unicode__(self):
        return 'Valid From: ' + str(self.valid_from)

    class Meta:
        verbose_name_plural = _('Grade Scale Validities')


# TODO send post save signal to change all available employee start time
# @receiver(post_save, sender=GradeScaleValidity)
# def incentive_account_category_add(sender, instance, created, **kwargs):
#     if created:
#         instance.account_category = Category.objects.create(
#             name='%s-%d' % (instance.name, instance.id),
#             parent=PayrollConfig.get_solo().incentive_account_category
#         )
#         instance.save()


class EmployeeGrade(models.Model):
    grade_name = models.CharField(max_length=100)
    grade_group = models.ForeignKey(
        EmployeeGradeGroup,
        null=True,
        blank=True,
        related_name="employee_grades"
    )

    # When employee is tecnician it should have no siblings
    is_technical = models.BooleanField(default=False)

    def __unicode__(self):
        if self.is_technical:
            return '%s-%s-%s' % (self.grade_group.name, self.grade_name, 'Technical')
        else:
            return '%s-%s' % (self.grade_group.name, self.grade_name)

    @property
    def name_unicode(self):
        return self.__unicode__()


class EmployeeGradeScale(models.Model):
    grade = models.ForeignKey(EmployeeGrade, related_name='grade_scales')
    salary_scale = models.FloatField()
    # rate increases yearly with grade rate. Also shold mention when in setting? How much times
    grade_number = models.PositiveIntegerField()
    grade_rate = models.FloatField()
    validity = models.ForeignKey(
        GradeScaleValidity,
        null=True,
        blank=True,
        related_name='grade_scales'
    )

    class Meta:
        unique_together = ('validity', 'grade')


class Designation(models.Model):
    designation_name = models.CharField(max_length=100, unique=True)
    grade = models.ForeignKey(EmployeeGrade)

    def __unicode__(self):
        return self.designation_name


class AllowanceName(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )
    code_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(
        max_length=250,
        verbose_name=_('Description')
    )
    is_tax_free = models.BooleanField(default=False)
    account_category = models.OneToOneField(Category, null=True, blank=True)

    # deduction_name_choices = (
    #     ('ACTIVE', _('Active')),
    #     ('INACTIVE', _('Inactive'))
    # )
    # status = models.CharField(max_length=20, choices=deduction_name_choices, default='ACTIVE')

    # def delete(self, *args, **kwargs):
    #     if self.account_category:
    #         self.account_category.delete()
    #     super(AllowanceName, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.name


class AllowanceValidity(models.Model):
    valid_from = HRBSDateField()
    note = models.CharField(max_length=150)

    # is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Valid From: ' + str(self.valid_from)

    class Meta:
        verbose_name_plural = _('Allowance Validities')


# TODO allowance validity
# This is bhatta
class Allowance(models.Model):
    name = models.ForeignKey(
        AllowanceName,
        null=True,
        blank=True,
        related_name="allowances"
    )
    employee_grade = models.ForeignKey(EmployeeGrade)
    sum_type = models.CharField(max_length=50, choices=deduct_choice)
    # Below is deduct type value
    value = models.FloatField()
    # amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? ==> May be it should be in settingShould be in setting
    payment_cycle = models.CharField(max_length=50, choices=payment_cycle)
    year_payment_cycle_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ],
    )
    validity = models.ForeignKey(
        AllowanceValidity,
        null=True,
        blank=True,
        related_name='allowances'
    )

    # def __unicode__(self):
    #     return '%s, %f' % (self.name, self.value)

    def save(self, *args, **kwargs):
        if self.payment_cycle is not 'Y':
            self.year_payment_cycle_month = None

        super(Allowance, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "employee_grade", 'validity'),)


class IncentiveName(models.Model):
    name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    account_category = models.OneToOneField(Category, null=True, blank=True)
    with_scale = models.BooleanField(default=False)
    amount_editable = models.BooleanField(default=False)
    is_tax_free = models.BooleanField(default=False)

    # deduction_name_choices = (
    #     ('ACTIVE', _('Active')),
    #     ('INACTIVE', _('Inactive'))
    # )
    # status = models.CharField(max_length=20, choices=deduction_name_choices, default='ACTIVE')

    def __unicode__(self):
        return self.name


class BranchOffice(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    address = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Office Branch')
        verbose_name_plural = _('Office Branches')


class PayrollAccountant(models.Model):
    user = models.OneToOneField(User, related_name='payroll_accountant')
    branch = TreeForeignKey(BranchOffice, related_name='payroll_accountants')

    def __unicode__(self):
        return str(self.user) + ' - ' + str(self.branch)


class DeductionValidity(models.Model):
    valid_from = HRBSDateField()
    note = models.CharField(max_length=150)

    def __unicode__(self):
        return 'Valid From: ' + str(self.valid_from)

    class Meta:
        verbose_name_plural = _('Deduction Validities')


class DeductionName(models.Model):
    # deduction_name_choices = (
    #     ('ACTIVE', _('Active')),
    #     ('INACTIVE', _('Inactive'))
    # )
    name = models.CharField(max_length=150)
    code_name = models.CharField(max_length=100, unique=True)

    deduct_in_category = models.OneToOneField(Category, null=True, blank=True)
    description = models.CharField(max_length=150)
    priority = models.IntegerField(unique=True)
    first_add_to_salary = models.BooleanField(default=False)
    # If true we can deduct while calculating taxable amount
    is_tax_free = models.BooleanField(default=False)

    is_optional = models.BooleanField(default=False)
    amount_editable = models.BooleanField(default=False)

    # status = models.CharField(max_length=20, choices=deduction_name_choices, default='ACTIVE')

    def __unicode__(self):
        return self.name

        # def delete(self, *args, **kwargs):
        #     if self.deduct_in_category:
        #         self.deduct_in_category.delete()
        #     super(DeductionName, self).delete(*args, **kwargs)


# These two below should be in setting as many to many
# Imp: Deductin cant be in BAnk Account type and should be one to one with account type
class Deduction(models.Model):
    name = models.ForeignKey(DeductionName)
    deduct_type = models.CharField(max_length=50, choices=deduct_choice)

    value = models.FloatField()

    validity = models.ForeignKey(DeductionValidity, blank=True, null=True)


# TODO make Employee Facility Crud
class EmployeeFacility(models.Model):
    name = models.CharField(max_length=100)
    rate = models.FloatField()

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    employee_type_choices = (
        ('PERMANENT', _('Permanent')),
        ('TEMPORARY', _('Temporary')),
    )
    status_choices = (
        ('ACTIVE', _('Active')),
        ('INACTIVE', _('Inactive')),
        ('SALARY_PUSED', _('Salary Paused')),
    )
    status = models.CharField(
        max_length=128,
        choices=status_choices,
        default="ACTIVE"
    )
    # Budget code (Functionality to change budget code for employee group)
    budget_code = models.CharField(max_length=100)
    pf_id_number = models.PositiveIntegerField(blank=True, null=True)
    insurance_id_number = models.PositiveIntegerField(blank=True, null=True)
    citizen_investment_id_number = models.PositiveIntegerField(blank=True, null=True)
    # working_branch = models.CharField(max_length=100)
    # Employee ko section or branch coz he can be in another branch and paid from central
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    type = models.CharField(max_length=128, choices=employee_type_choices)
    marital_statuses = [('M', _('Married')), ('U', _('Unmarried'))]
    name = models.CharField(max_length=128)
    code_name = models.CharField(max_length=100, unique=True)
    sex = models.CharField(choices=sex_choice, max_length=1)
    marital_status = models.CharField(
        default='U',
        max_length=1,
        choices=marital_statuses
    )
    designation = models.ForeignKey(Designation)
    pan_number = models.CharField(max_length=100)
    working_branch = TreeForeignKey(BranchOffice, related_name='branch_employees')

    # TODO see this accounts
    accounts = models.ManyToManyField(Account, through="EmployeeAccount")

    # BankDetails
    bank = models.ForeignKey(Bank, related_name='employees', null=True, blank=True)
    bank_branch = models.ForeignKey(BankBranch, related_name='employees', null=True, blank=True)
    bank_account_number = models.CharField(max_length=256)
    # BankDetailsEnd

    appoint_date = HRBSDateField(null=True, blank=True)
    # On newly apponted employee appoint date and scale start date will be same
    # On previous employee(employee working before this software arrival appoint date be null and salary scale date be calculated)
    # Scale start date can also be added manually

    # This is point to start salary calculation
    # May need during new user entry or import
    # if below field is not present then given from date validity start from is used
    scale_start_date = HRBSDateField()

    dismiss_date = HRBSDateField(null=True, blank=True)
    yearly_insurance_premium = models.FloatField(default=0.0)
    is_disabled_person = models.BooleanField(default=False)

    grade_number = models.PositiveIntegerField()
    # allowance will be added to salary
    allowances = models.ManyToManyField(AllowanceName, blank=True)
    # incentive will have diff trancation
    incentives = models.ManyToManyField(IncentiveName, blank=True, through="Incentive")

    optional_deductions = models.ManyToManyField(
        DeductionName,
        blank=True
    )
    facilities = models.ManyToManyField(EmployeeFacility, blank=True)

    class Meta:
        unique_together = (('bank', 'bank_branch', 'bank_account_number'),)
        verbose_name = _('Employee')

    def excluded_days_for_grade_pause(self, scale_start_date, check_upto_date):
        excluded_days = 0
        if isinstance(scale_start_date, date):
            filter = {
                'from_date__gte': scale_start_date
            }
        else:
            filter = {
                'from_date__gte': scale_start_date.as_ad()
            }
        for gnp in self.grade_number_pause_details.filter(**filter):
            if check_upto_date < gnp.from_date:
                pass
            elif check_upto_date >= gnp.from_date and check_upto_date <= gnp.to_date:
                diff = check_upto_date - gnp.from_date
                excluded_days += diff.days

            elif check_upto_date > gnp.to_date:
                diff = gnp.to_date - gnp.from_date
                excluded_days += diff.days + 1
        return excluded_days

    def get_grade_number(self, upto_date):
        '''
        if upto date is last of month den do nothing
        if first of month then drc date by one day
        :param upto_date:
        :return:
        '''
        upto_date = drc_1_day(upto_date)
        grade_validity_slots = get_validity_slots(GradeScaleValidity, self.scale_start_date, upto_date)
        current_addition = 0
        current_grade_number = 0
        for slot in grade_validity_slots:
            rate_obj = EmployeeGradeScale.objects.filter(
                validity_id=slot.validity_id,
                grade=self.designation.grade
            )[0]
            # slot_scale = rate_obj.salary_scale
            slot_rate = rate_obj.grade_rate
            slot_initial_number = math.ceil(float(current_addition) / float(slot_rate))

            days_worked = slot.to_date - slot.from_date
            years_worked = ((days_worked.days + 1) - self.excluded_days_for_grade_pause(slot.from_date,
                                                                                        slot.to_date)) / 365
            current_grade_number += years_worked + slot_initial_number
            current_addition += current_grade_number * slot_rate
        return current_grade_number

    def current_salary_by_month(self, from_date, to_date, **kwargs):

        rate_obj = EmployeeGradeScale.objects.filter(
            validity_id=kwargs['validity_id'],
            grade=self.designation.grade
        )[0]

        grade_salary = rate_obj.salary_scale
        grade_number = self.grade_number if self.grade_number < rate_obj.grade_number else rate_obj.grade_number
        grade_rate = rate_obj.grade_rate
        salary = 0
        grade_amount = 0
        for year, month in get_y_m_tuple_list(from_date, to_date):
            if type(from_date) == type(to_date):
                # scale_start_date = self.get_scale_start_date(from_date)
                if isinstance(from_date, date):
                    try:
                        days_worked = date(year, month, 1) - self.scale_start_date
                        upto_date = date(year, month, 1)
                    except:
                        raise TypeError('Internal and external setting mismatch')
                else:
                    if isinstance(self.scale_start_date, date):
                        raise TypeError('Internal and external setting mismatch')
                    else:
                        # TODO think whether it is upto beggining of month or last of month
                        days_worked = date(*bs2ad(date(year, month, 1))) - date(
                            *bs2ad((self.scale_start_date.as_string())))
                        upto_date = BSDate(year, month, 1)

            # years_worked = (days_worked.days - self.excluded_days_for_grade_pause(scale_start_date, upto_date)) / 365
            computed_grade_number = self.get_grade_number(upto_date)
            # the above will work for both appointed and old employee with no change in salary scale
            # Everything gets diffent when salary scale sheet is ammended
            if kwargs.get('apply_grade_rate'):
                if computed_grade_number <= grade_number:
                    salary += grade_salary + int(computed_grade_number) * grade_rate
                    grade_amount += int(computed_grade_number) * grade_rate
                elif computed_grade_number > grade_number:
                    salary += grade_salary + grade_number * grade_rate
                    grade_amount += grade_number * grade_rate
            else:
                salary += grade_salary
        return salary, grade_amount

    def get_date_range_salary(self, from_date, to_date, **kwargs):
        try:
            validity_slots = get_validity_slots(GradeScaleValidity, from_date, to_date)
        except IOError:
            raise
        salary = 0
        grade_amount = 0
        for slot in validity_slots:
            kwargs['validity_id'] = slot.validity_id
            sal, gra = self.current_salary_by_day(slot.from_date, slot.to_date, **kwargs)
            salary += sal
            grade_amount += gra

        if kwargs.get('get_grade_number'):
            return grade_amount
        return salary

    def current_salary_by_day(self, from_date, to_date, **kwargs):
        if from_date.year == to_date.year and from_date.month == to_date.month:
            salary_pure_months = 0
            pure_month_grade_amount = 0
            lhs_month_salary = 0
            lhs_month_grade_amount = 0
            lhs_days = 0
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    month = date(from_date.year, from_date.month, 1)
                    # We need to add because from and to in same month
                    # Will be different when many months
                    # because we cut them to slots
                    rhs_days = (to_date - from_date).days + 1

                    from_date_month_days = mr(month.year, month.month)[1]
                    to_date_month_days = from_date_month_days
                else:
                    month = BSDate(from_date.year, from_date.month, 1)
                    rhs_days = (to_date - from_date).days + 1
                    from_date_month_days = bs[month.year][month.month - 1]
                    to_date_month_days = from_date_month_days
                    # pdb.set_trace()

            rhs_month_salary, rhs_month_grade_amount = self.current_salary_by_month(
                month,
                month,
                **kwargs
            )

        elif are_side_months(from_date, to_date):
            salary_pure_months = 0
            pure_month_grade_amount = 0
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    lhs_month = date(from_date.year, from_date.month, 1)
                    rhs_month = date(to_date.year, to_date.month, 1)
                    lhs_days = (rhs_month - from_date).days
                    rhs_days = (to_date - rhs_month).days + 1

                    from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                    to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

                else:
                    lhs_month = BSDate(from_date.year, from_date.month, 1)
                    rhs_month = BSDate(to_date.year, to_date.month, 1)
                    lhs_days = (rhs_month - from_date).days
                    rhs_days = (to_date - rhs_month).days + 1

                    from_date_month_days = bs[lhs_month.year][lhs_month.month - 1]
                    to_date_month_days = bs[rhs_month.year][rhs_month.month - 1]
            lhs_month_salary, lhs_month_grade_amount = self.current_salary_by_month(
                lhs_month,
                lhs_month,
                **kwargs
            )
            rhs_month_salary, rhs_month_grade_amount = self.current_salary_by_month(
                rhs_month,
                rhs_month,
                **kwargs
            )
        else:
            # Get pure months
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    if from_date.month == 12:
                        from_date_m = date(from_date.year + 1, 1, 1)
                    else:
                        from_date_m = date(from_date.year, from_date.month + 1, 1)
                    if to_date.month == 1:
                        to_date_m = date(to_date.year - 1, 12, 1)
                    else:
                        to_date_m = date(to_date.year, to_date.month - 1, 1)
                    lhs_month = date(from_date.year, from_date.month, 1)
                    rhs_month = date(to_date.year, to_date.month, 1)
                    lhs_days = (from_date_m - from_date).days
                    rhs_days = (to_date - to_date_m).days + 1

                    from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                    to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

                else:
                    if from_date.month == 12:
                        from_date_m = BSDate(from_date.year + 1, 1, 1)
                    else:
                        from_date_m = BSDate(from_date.year, from_date.month + 1, 1)
                    if to_date.month == 1:
                        to_date_m = BSDate(to_date.year - 1, 12, 1)
                    else:
                        to_date_m = BSDate(to_date.year, to_date.month - 1, 1)
                    lhs_month = BSDate(from_date.year, from_date.month, 1)
                    rhs_month = BSDate(to_date.year, to_date.month, 1)
                    lhs_days = (from_date_m - from_date).days
                    rhs_days = (to_date - to_date_m).days + 1

                    from_date_month_days = bs[lhs_month.year][lhs_month.month - 1]
                    to_date_month_days = bs[rhs_month.year][rhs_month.month - 1]

            salary_pure_months, pure_month_grade_amount = self.current_salary_by_month(
                from_date_m,
                to_date_m,
                **kwargs
            )
            lhs_month_salary, lhs_month_grade_amount = self.current_salary_by_month(
                lhs_month,
                lhs_month,
                **kwargs
            )
            rhs_month_salary, rhs_month_grade_amount = self.current_salary_by_month(
                rhs_month,
                rhs_month,
                **kwargs
            )
        lhs_salary = lhs_month_salary / float(from_date_month_days) * lhs_days
        rhs_salary = rhs_month_salary / float(to_date_month_days) * rhs_days
        salary = salary_pure_months + lhs_salary + rhs_salary

        lhs_grade_amount = lhs_month_grade_amount / float(from_date_month_days) * lhs_days
        rhs_grade_amount = rhs_month_grade_amount / float(to_date_month_days) * rhs_days
        total_grade_amount = pure_month_grade_amount + lhs_grade_amount + rhs_grade_amount

        return salary, total_grade_amount

    def has_account(self, account_type):
        for i in self.accounts.all():
            if i.employee_account.other_account_type == account_type:
                return True
        return False

    def __unicode__(self):
        return self.name


class EmployeeGradeNumberPause(models.Model):
    employee = models.ForeignKey(Employee, related_name='grade_number_pause_details')
    from_date = HRBSDateField()
    to_date = HRBSDateField()

    def delete(self):
        employee_last_paid = employee_last_payment_record(self.employee)
        if not employee_last_paid:
            employee_last_paid = drc_1_day(self.employee.scale_start_date)
        if (
                        employee_last_paid >= self.from_date and employee_last_paid <= self.to_date) or employee_last_paid > self.to_date:
            pass
        else:
            super(EmployeeGradeNumberPause, self).delete()

    def __unicode__(self):
        return '%s-to-%s' % (self.from_date, self.to_date)


# This is incentive(for motivation)
class Incentive(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.ForeignKey(
        IncentiveName,
        null=True,
        blank=True,
        related_name='incentives'
    )
    employee = models.ForeignKey(Employee)
    # Any one of the two should be filled
    sum_type = models.CharField(max_length=50, choices=deduct_choice)
    # Below is deduct type value
    value = models.FloatField(null=True, blank=True)
    # amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? == May be we should keep it in setting
    # payment_cycle = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    payment_cycle = models.CharField(max_length=50, choices=payment_cycle)
    year_payment_cycle_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ],
    )

    def __unicode__(self):
        if self.sum_type == 'AMOUNT':
            return '%s[Amount] %f' % (self.name, self.value)
        elif self.sum_type == 'RATE':
            return '%s[Amount] %f' % (self.name, self.value)
        else:
            return '%s-NOTFIXED' % (self.name)

    def save(self, *args, **kwargs):
        if self.payment_cycle != 'Y':
            self.year_payment_cycle_month = None
        super(Incentive, self).save(*args, **kwargs)

    # TODO error when not unique not displayed because global errors not shown
    class Meta:
        unique_together = (("name", "employee"),)


# FIXME not proper entry validate properly
class ProTempore(models.Model):
    status_choices = (
        ('REGISTERED', _('Registered')),
        ('READY_FOR_PAYMENT', _('Ready for Payment')),
        ('PAID', _('Paid')),
    )
    employee = models.OneToOneField(Employee,
                                    related_name="real_employee_post")
    pro_tempore_employee = models.OneToOneField(Employee,
                                                related_name="virtual_employee_post")
    appoint_date = HRBSDateField(default=today)
    dismiss_date = HRBSDateField(null=True, blank=True)
    status = models.CharField(max_length=128, choices=status_choices, default='REGISTERED')

    def __unicode__(self):
        return str(self.id)


class MaritalStatus(models.Model):
    marital_statuses = [('M', _('Married')), ('U', _('Unmarried'))]
    marital_status = models.CharField(
        default='U',
        max_length=1,
        choices=marital_statuses,
        unique=True
    )

    def __unicode__(self):
        return str('MARRIED' if self.marital_status == 'M' else 'UNMARRIED')


class TaxDeduction(models.Model):
    code_name_choices = [
        ('Remuneration Tax', _('Remuneration Tax')),
        ('Social Security Tax', _('Social Security Tax'))
    ]
    name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100, choices=code_name_choices, unique=True)
    account_category = models.OneToOneField(Category, null=True, blank=True)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class IncomeTaxScheme(models.Model):
    # marital_statuses = [('M', _('Married')), ('U', _('Unmarried'))]
    marital_status = models.ForeignKey(
        MaritalStatus,
        related_name="tax_scheme"
    )
    start_from = models.FloatField()
    end_to = models.FloatField(null=True, blank=True)
    # tax_rate = models.FloatField()
    priority = models.PositiveIntegerField()

    def __unicode__(self):
        return u"From %s" % str(self.start_from)

    class Meta:
        unique_together = (
            ('marital_status', 'start_from', 'end_to'),
            ('marital_status', 'priority')
        )


class IncomeTaxCalcScheme(models.Model):
    scheme = models.ForeignKey(
        IncomeTaxScheme,
        related_name="tax_calc_scheme"
    )
    start_from = models.FloatField()
    end_to = models.FloatField(null=True, blank=True)
    tax_rate = models.FloatField()
    priority = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            ('scheme', 'start_from', 'end_to'),
            ('scheme', 'priority')
        )


class PayrollEntry(models.Model):
    # entry_rows = models.ManyToManyField(PaymentRecord)

    paid_from_date = HRBSDateField()
    paid_to_date = HRBSDateField()

    branch = TreeForeignKey(BranchOffice, related_name='payroll_entries')
    is_monthly_payroll = models.BooleanField(default=False)
    entry_datetime = models.DateTimeField(default=timezone.now)
    entry_date = HRBSDateField(default=today)
    approved = models.BooleanField(default=False)
    transacted = models.BooleanField(default=False)

    def __unicode__(self):
        if self.branch:
            branch_name = self.branch.name
        else:
            branch_name = "All branch"
        if self.is_monthly_payroll:
            typ = "Monthly"
        else:
            typ = "Custom Date range"
        timestamp = 'From %s to %s' % (self.paid_from_date, self.paid_to_date)
        return '%s-%s-%s-Entry on %s. ' % (
            branch_name,
            typ,
            timestamp,
            str(self.entry_datetime),
        )

        # TODO uncomment delete function after transaction testing is done
        # def delete(self, *args, **kwargs):
        #     if self.transacted:
        #         pass
        #     else:
        #         super(PayrollEntry, self).delete(*args, **kwargs)


class PaymentRecord(models.Model):
    entry = models.ForeignKey(PayrollEntry, related_name='entry_rows')
    paid_employee = models.ForeignKey(Employee)
    designation = models.ForeignKey(Designation)
    paid_from_date = HRBSDateField()
    paid_to_date = HRBSDateField()
    absent_days = models.PositiveIntegerField()
    allowance = models.FloatField(null=True, blank=True)
    incentive = models.FloatField(null=True, blank=True)
    deduced_amount = models.FloatField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField()

    # Deducted amount fields
    # How much incentive and how much allowance

    def total_present_days(self):
        return self.paid_to_date - self.paid_from_date - self.absent_days

    def __unicode__(self):
        return 'payment-record-#%s' % (self.id)


    @property
    def months_in_range(self):
        return get_y_m_in_words(self.paid_from_date, self.paid_to_date)

    @property
    def pro_tempore_amount(self):
        total = 0
        for pt in self.pro_tempore_details.all():
            total += pt.amount
        return total

    @property
    def grade_amount(self):
        amount = self.paid_employee.get_date_range_salary(
            self.paid_from_date,
            self.paid_to_date,
            get_grade_number=True,
            apply_grade_rate=True
        )
        return amount

    @property
    def total_after_addition(self):
        total_addition_in_deduction = 0
        for deduction_detail in self.deduction_details.all():
            total_addition_in_deduction += deduction_detail.amount_added_before_deduction
        return self.salary + total_addition_in_deduction

    @property
    def total_after_allowance_addition(self):
        return self.total_after_addition + self.allowance

    @property
    def total_tax(self):
        total_tax = 0
        for tax_detail in self.tax_details.all():
            total_tax += tax_detail.amount
        return total_tax

    @property
    def total_deduction_inc_tax(self):
        return self.deduced_amount + self.total_tax



class DeductionDetail(models.Model):
    deduction = models.ForeignKey(
        DeductionName,
        related_name='deduced_amount_detail'
    )
    amount = models.FloatField()
    amount_added_before_deduction = models.FloatField(default=0.0)
    payment_record = models.ForeignKey(PaymentRecord, related_name='deduction_details')

    def __unicode__(self):
        return "%s-[%s]" % (self.deduction.name, str(self.amount))


    @property
    def compulsory_deduction(self):
        return self.amount - self.amount_added_before_deduction


class IncentiveDetail(models.Model):
    incentive = models.ForeignKey(
        IncentiveName,
        related_name='incentive_amount_detail'
    )
    amount = models.FloatField()
    payment_record = models.ForeignKey(PaymentRecord, related_name='incentive_details')


class AllowanceDetail(models.Model):
    allowance = models.ForeignKey(
        AllowanceName,
        related_name='allowance_amount_detail'
    )
    amount = models.FloatField()
    payment_record = models.ForeignKey(PaymentRecord, related_name='allowance_details')


class ProTemporeDetail(models.Model):
    pro_tempore = models.OneToOneField(ProTempore, related_name='pro_tempore_record')
    amount = models.FloatField()
    payment_record = models.ForeignKey(PaymentRecord, related_name='pro_tempore_details')

    @property
    def appoint_date(self):
        return str(self.pro_tempore.appoint_date)

    @property
    def dismiss_date(self):
        return str(self.pro_tempore.dismiss_date)


class TaxDetail(models.Model):
    tax_deduction = models.ForeignKey(TaxDeduction, related_name='tax_details')
    amount = models.FloatField()
    payment_record = models.ForeignKey(PaymentRecord, related_name='tax_details')


def employee_account_validator(acc_id):
    category = Account.objects.get(id=acc_id).category
    if category == PayrollConfig.get_solo().basic_salary_account_category or category.parent.parent == PayrollConfig.get_solo().pay_head_account_category or category.parent == PayrollConfig.get_solo().pay_head_account_category:
        pass
    else:
        raise ValidationError(
            _('Account must be of Category BASIC SALARY or DEDUCTION'),
        )


class EmployeeAccount(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='employee_account',
        validators=[employee_account_validator]
    )

    def __unicode__(self):
        return '%s-%s-%s' % (self.employee.name, self.account.category.name, self.account.name)

    class Meta:
        unique_together = (("employee", "account"),)

    def get_category_name(self):
        return self.account.category.name


class ReportHR(models.Model):
    hr_report_template_folder = BASE_DIR + '/hr/templates/report_templates'
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    template = models.FilePathField(path=hr_report_template_folder, match=".*\.html$")
    # for_employee_type = models.CharField(max_length=50, choices=emp_type_choices)
    
    def __unicode__(self):
        return self.name


class ReportTable(models.Model):
    title = models.CharField(max_length=100)
    # # field_tiltle and field loopup sored as Json
    # report_table_json_folder = BASE_DIR + '/hr/templates/report_templates/report_table_jsons'
    # table_json = models.FilePathField(path=report_table_json_folder, match=".*\.json$")
    # # table_fields = JSONField()
    report = models.ForeignKey(ReportHR, related_name='report_tables')

    def __unicode__(self):
        return self.title


class ReportTableDetail(models.Model):
    field_name = models.CharField(max_length=250)
    field_description = models.CharField(max_length=500)
    order = models.PositiveIntegerField()
    need_total = models.BooleanField(default=False)
    table = models.ForeignKey(ReportTable, related_name='table_details')

    def __unicode__(self):
        return self.field_name

    class Meta:
        unique_together = (('order', 'table'),)


class PayrollConfig(SingletonModel):
    calendar_choices = (
        ('BS', 'BS'),
        ('AD', 'AD'),
    )
    parent_can_generate_payroll = models.BooleanField(default=False)
    # TODO below can only be changed when hr has no entries in datefield model

    organization_title = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    hr_calendar = models.CharField(max_length=2, choices=calendar_choices, default='BS')
    pay_head_account_category = TreeOneToOneField(Category, related_name='config_pay_head', null=True, blank=True)
    deduction_account_category = TreeOneToOneField(Category, related_name='config_deduction', null=True, blank=True)
    allowance_account_category = TreeOneToOneField(Category, related_name='config_allowance', null=True, blank=True)
    incentive_account_category = TreeOneToOneField(Category, related_name='config_incentive', null=True, blank=True)
    basic_salary_account_category = TreeOneToOneField(Category, related_name='config_basic_salary', null=True,
                                                      blank=True)
    tax_account_category = TreeOneToOneField(Category, related_name='config_tax', null=True, blank=True)
    salary_giving_account_category = TreeOneToOneField(Category, related_name='config_salary_giving', null=True,
                                                       blank=True)
    pro_tempore_account_category = TreeOneToOneField(Category, related_name='config_pro_tempore', null=True, blank=True)

    # Taxation settings global
    married_remuneration_discount = models.FloatField(
        default=300000.0,
        verbose_name=_('Remuneration tax discount for married employee on taxable amount.')
    )
    unmarried_remuneration_discount = models.FloatField(
        default=300000.0,
        verbose_name=_('Remuneration tax discount for unmarried employee on taxable amount.')
    )

    # below field is in percentage
    disabled_remuneration_additional_discount = models.FloatField(
        default=50,
        verbose_name=_('Remuneration tax additional discount for disabled employee on taxable amount.(%)')
    )
    female_remuneration_tax_discount = models.FloatField(
        default=10,
        verbose_name=_('Discount for female on evaluated remuneration tax. (%)')
    )

    def __unicode__(self):
        return "Payroll Configuration"

    class Meta:
        verbose_name = "Payroll Configuration"


# Models Signals
@receiver(post_save, sender=AllowanceName)
def allowance_account_category_add(sender, instance, created, **kwargs):
    if created:
        instance.account_category = Category.objects.create(
            name=instance.code_name,
            parent=PayrollConfig.get_solo().allowance_account_category
        )
        instance.save()
    else:
        if instance.account_category:
            instance.account_category.name = instance.code_name
            instance.account_category.save()


@receiver(post_save, sender=IncentiveName)
def incentive_account_category_add(sender, instance, created, **kwargs):
    if created:
        instance.account_category = Category.objects.create(
            name=instance.code_name,
            parent=PayrollConfig.get_solo().incentive_account_category
        )
        instance.save()
    else:
        if instance.account_category:
            instance.account_category.name = instance.code_name
            instance.account_category.save()


@receiver(post_save, sender=DeductionName)
def deduct_in_category_add(sender, instance, created, **kwargs):
    if created:
        instance.deduct_in_category = Category.objects.create(
            name=instance.code_name,
            parent=PayrollConfig.get_solo().deduction_account_category
        )
        # Add newly created deduction accout for existing user
        if not instance.is_optional:
            for emp in Employee.objects.all():
                acc = Account.objects.create(
                    name='%s-%s' % (emp.name, instance.code_name),
                    category=instance.deduct_in_category,
                    fy=FiscalYear.get()
                )
                EmployeeAccount.objects.create(
                    account=acc,
                    employee=emp
                )

        if instance.first_add_to_salary:
            add_before_deduction_cat = Category.objects.create(
                name='%s addition in deduction' % instance.code_name,
                parent=instance.deduct_in_category,
                # fy=FiscalYear.get()
            )

            if not instance.is_optional:
                for emp in Employee.objects.filter(type='PERMANENT'):
                    acc = Account.objects.create(
                        name='%s-AddBeforeDedution-%s' % (emp.code_name, instance.code_name),
                        category=add_before_deduction_cat,
                        fy=FiscalYear.get()
                    )
                    EmployeeAccount.objects.create(
                        account=acc,
                        employee=emp
                    )
        instance.save()

    else:
        if instance.deduct_in_category:
            instance.deduct_in_category.name = instance.code_name
            instance.deduct_in_category.save()

            # Add newly created deduction accout for existing user
            if not instance.is_optional:
                for emp in Employee.objects.all():
                    acc = Account.objects.get_or_create(
                        name='%s-%s' % (emp.code_name, instance.code_name),
                        category=instance.deduct_in_category,
                        fy=FiscalYear.get(),
                        employee_account__employee=emp
                    )
                    EmployeeAccount.objects.get_or_create(
                        account=acc,
                        employee=emp
                    )

            addition_from_deduction_cats = instance.deduct_in_category.children.all()
            if instance.first_add_to_salary:
                if not addition_from_deduction_cats:
                    addition_from_deduction_cat = Category.objects.create(
                        name='%s addition in deduction' % instance.code_name,
                        parent=instance.deduct_in_category
                    )
                else:
                    addition_from_deduction_cats[0].name = '%s addition in deduction' % instance.code_name
                    addition_from_deduction_cats[0].save()
                    addition_from_deduction_cat = addition_from_deduction_cats[0]

                if not instance.is_optional:
                    for emp in Employee.objects.filter(type='PERMANENT'):
                        acc, created = Account.objects.get_or_create(
                            name='%s-AddBeforeDedution-%s' % (emp.code_name, instance.code_name),
                            category=addition_from_deduction_cat,
                            fy=FiscalYear.get(),
                            employee_account__employee=emp
                        )
                        EmployeeAccount.objects.get_or_create(
                            account=acc,
                            employee=emp
                        )
                        # else:
                        #     if addition_from_deduction_cats:
                        #         addition_from_deduction_cats[0].delete()


@receiver(m2m_changed, sender=Employee.optional_deductions.through)
def on_optional_deductions_change(sender, instance, action, **kwargs):
    if action == 'post_add':
        for this_deduction in instance.optional_deductions.all():
            this_deduction_emp_accs = EmployeeAccount.objects.filter(
                account__name='%s-%s' % (instance.code_name, this_deduction.code_name),
                account__category=this_deduction.deduct_in_category,
                account__fy=FiscalYear.get(),
                employee=instance
            )
            if not this_deduction_emp_accs:
                opt_deduction_account = Account.objects.create(
                    name='%s-%s' % (instance.code_name, this_deduction.code_name),
                    category=this_deduction.deduct_in_category,
                    fy=FiscalYear.get()
                )
                EmployeeAccount.objects.create(
                    account=opt_deduction_account,
                    employee=instance,
                )
        if instance.type == 'PERMANENT':
            for this_deduction in instance.optional_deductions.filter(first_add_to_salary=True):
                add_before_deduction_emp_acc = EmployeeAccount.objects.filter(
                    account__name='%s-AddBeforeDedution-%s' % (instance.code_name, this_deduction.code_name),
                    account__category=this_deduction.deduct_in_category.children.all()[0],
                    account__fy=FiscalYear.get(),
                    employee=instance
                )
                if not add_before_deduction_emp_acc:
                    add_before_deduction_account = Account.objects.create(
                        name='%s-AddBeforeDedution-%s' % (instance.code_name, this_deduction.code_name),
                        category=this_deduction.deduct_in_category.children.all()[0],
                        fy=FiscalYear.get()
                    )
                    EmployeeAccount.objects.create(
                        account=add_before_deduction_account,
                        employee=instance,
                    )


@receiver(m2m_changed, sender=Employee.allowances.through)
def on_allowances_change(sender, instance, action, **kwargs):
    if action == 'post_add':
        for this_allowance in instance.allowances.all():
            this_allowance_emp_accs = EmployeeAccount.objects.filter(
                account__name='%s-%s' % (instance.code_name, this_allowance.code_name),
                account__fy=FiscalYear.get(),
                account__category=this_allowance.account_category,
                employee=instance
            )
            if not this_allowance_emp_accs:
                all_account = Account.objects.create(
                    name='%s-%s' % (instance.code_name, this_allowance.code_name),
                    category=this_allowance.account_category,
                    fy=FiscalYear.get()
                )
                EmployeeAccount.objects.create(
                    account=all_account,
                    employee=instance,
                )


@receiver(post_save, sender=Employee)
def add_employee_accounts(sender, instance, created, **kwargs):
    if created:
        # Add salary Account
        salary_account = Account.objects.create(
            name="%s-Salary Account" % instance.code_name,
            category=PayrollConfig.get_solo().basic_salary_account_category,
            fy=FiscalYear.get()
        )
        EmployeeAccount.objects.create(
            account=salary_account,
            employee=instance,
        )

        # Add tax deduction account
        for tax_deduction in TaxDeduction.objects.all():
            td_account = Account.objects.create(
                name='%s-%s' % (instance.code_name, tax_deduction.code_name),
                category=tax_deduction.account_category,
                fy=FiscalYear.get()
            )

            EmployeeAccount.objects.create(
                account=td_account,
                employee=instance,
            )

        # Add pro tempore account
        pro_tempore_account = Account.objects.create(
            name="%s-ProTempore" % instance.code_name,
            category=PayrollConfig.get_solo().pro_tempore_account_category,
            fy=FiscalYear.get()
        )
        EmployeeAccount.objects.create(
            account=pro_tempore_account,
            employee=instance,
        )
        # Add deduction accounts (compulsory)
        for deduction in DeductionName.objects.filter(is_optional=False):
            deduction_account = Account.objects.create(
                name="%s-%s" % (
                    instance.code_name,
                    deduction.code_name
                ),
                category=deduction.deduct_in_category,
                fy=FiscalYear.get()
            )
            EmployeeAccount.objects.create(
                account=deduction_account,
                employee=instance,
            )
        if instance.type == 'PERMANENT':
            for deduction in DeductionName.objects.filter(is_optional=False, first_add_to_salary=True):
                add_before_deduction_account = Account.objects.create(
                    name='%s-AddBeforeDedution-%s' % (instance.code_name, deduction.code_name),
                    category=deduction.deduct_in_category.children.all()[0],
                    fy=FiscalYear.get()
                )
                EmployeeAccount.objects.create(
                    account=add_before_deduction_account,
                    employee=instance,
                )
    else:
        employee_accounts = EmployeeAccount.objects.filter(employee=instance)
        for emp_account in employee_accounts:
            if emp_account.account.category == PayrollConfig.get_solo().basic_salary_account_category:
                emp_account.account.name = "%s-Salary Account" % instance.code_name
                emp_account.account.save()

            if emp_account.account.category == PayrollConfig.get_solo().pro_tempore_account_category:
                emp_account.account.name = "%s-ProTempore" % instance.code_name
                emp_account.account.save()

            for tax_deduction in TaxDeduction.objects.all():
                if emp_account.account.category == tax_deduction.account_category:
                    emp_account.account.name = '%s-%s' % (instance.code_name, tax_deduction.code_name)
                    emp_account.account.save()

            for deduction in DeductionName.objects.filter(is_optional=False):
                if emp_account.account.category == deduction.deduct_in_category:
                    emp_account.account.name = "%s-%s" % (
                        instance.code_name,
                        deduction.code_name
                    )
                    emp_account.account.save()
            for this_deduction in instance.optional_deductions.all():
                if emp_account.account.category == this_deduction.deduct_in_category:
                    emp_account.account.name = "%s-%s" % (
                        instance.code_name,
                        this_deduction.code_name
                    )
                    emp_account.account.save()

            for this_allowance in instance.allowances.all():
                if emp_account.account.category == this_allowance.account_category:
                    emp_account.account.name = "%s-%s" % (
                        instance.code_name,
                        this_allowance.code_name
                    )
                    emp_account.account.save()

            for incentive in instance.incentives.all():
                if emp_account.account.category == incentive.account_category:
                    emp_account.account.name = "%s-%s" % (
                        instance.code_name,
                        incentive.code_name
                    )
                    emp_account.account.save()


        if instance.type == 'PERMANENT':
            for deduction in DeductionName.objects.filter(is_optional=False, first_add_to_salary=True):
                add_before_deduction_account, created = Account.objects.get_or_create(
                    name='%s-AddBeforeDedution-%s' % (instance.code_name, deduction.code_name),
                    category=deduction.deduct_in_category.children.all()[0],
                    fy=FiscalYear.get(),
                    employee_account__employee=instance
                )
                EmployeeAccount.objects.get_or_create(
                    account=add_before_deduction_account,
                    employee=instance,
                )


@receiver(post_save, sender=Incentive)
def add_emloyee_incentive_account(sender, instance, created, **kwargs):
    if created:
        this_incentive_emp_accs = EmployeeAccount.objects.filter(
            account__name='%s-%s' % (instance.employee.code_name, instance.name.code_name),
            account__fy=FiscalYear.get(),
            account__category=instance.name.account_category,
            employee=instance.employee
        )
        if not this_incentive_emp_accs:
            incent_account = Account.objects.create(
                name='%s-%s' % (instance.employee.code_name, instance.name.code_name),
                category=instance.name.account_category,
                fy=FiscalYear.get()
            )
            EmployeeAccount.objects.create(
                account=incent_account,
                employee=instance.employee,
            )


@receiver(post_save, sender=TaxDeduction)
def account_category_add(sender, instance, created, **kwargs):
    if created:
        instance.account_category = Category.objects.create(
            name=instance.code_name,
            parent=PayrollConfig.get_solo().tax_account_category
        )

        for emp in Employee.objects.all():
            acc = Account.objects.create(
                name='%s-%s' % (emp.code_name, instance.code_name),
                category=instance.account_category,
                fy=FiscalYear.get()
            )
            EmployeeAccount.objects.create(
                account=acc,
                employee=emp
            )
        instance.save()

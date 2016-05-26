# import dbsettings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
# from core.models import validate_in_fy
from njango.fields import BSDateField, today
from njango.nepdate import bs2ad, bs
from django.core.validators import MaxValueValidator, MinValueValidator
from calendar import monthrange as mr
from datetime import date
import datetime
from hr.bsdate import BSDate
from .helpers import get_y_m_tuple_list, are_side_months, zero_for_none, none_for_zero
from django.core.exceptions import ValidationError
# import pdb


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import F
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import pdb

from account.models import Account, Category
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
# from core.models import FiscalYear
# from solo.models import SingletonModel
# from django.core.exceptions import ValidationError


# def validate_month(value):
#     if value < 1 and value > 12:
#         raise ValidationError(
#             _('%(value)s is not'),
#             params={'value': value},
#         )

# Account type name should be same as fieldname in employee account with small letter and underscope
# That is field name for 'BANK ACCOUNT' in employee model 
# will be 'bank_account'
acc_type = [('insurance_account', _('Insurance Account')),
            ('nalakosh_account', _('Nagarik Lagani Kosh Account')),
            ('sanchayakosh_account', _('Sanchayakosh Account'))]
deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
deduct_from = [('EMPLOYEE ACC', _('For employee Account')),
              ('EXPLICIT ACC', _('An Explicit Account'))]
payment_cycle = [('M', _('Monthly')),
                 ('Y', _('Yearly')),
                 ('D', _('Daily')),
                 ]
holder_type = [('EMPLOYEE', _("Employee's Account")),
               ('COMPANY', _('Company Account'))]

# Accout Category settingShoul
ACC_CAT_DEDUCTION_ID = 5
ACC_CAT_ALLOWANCE_ID = 4
ACC_CAT_INCENTIVE_ID = 6
ACC_CAT_BASIC_SALARY_ID = 3
ACC_CAT_TAX_ID = 7

# allowance
# When yearly than when to pay should be in setting


class AccountType(models.Model):
    name = models.CharField(max_length=150, choices=acc_type, unique=True)
    description = models.CharField(max_length=250)
    permanent_multiply_rate = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name


class EmployeeGrade(models.Model):
    grade_name = models.CharField(max_length=100)
    salary_scale = models.FloatField()
    # rate increases yearly with grade rate. Also shold mention when in setting? How much times
    grade_number = models.PositiveIntegerField()
    grade_rate = models.FloatField()
    parent_grade = models.ForeignKey('self', null=True, blank=True)
    # When employee is tecnician it should have no siblings
    is_technical = models.BooleanField(default=False)

    def __unicode__(self):
        if self.is_technical:
            return self.grade_name + '( Is Tecnician)'
        else:
            return self.grade_name


class Designation(models.Model):
    designation_name = models.CharField(max_length=100)
    grade = models.ForeignKey(EmployeeGrade)

    def __unicode__(self):
        return self.designation_name


class DeductionAccount(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='deduction_ledger'
    )

    def __unicode__(self):
        return self.account.name


class AllowanceAccount(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='allowance_ledger'
    )

    def __unicode__(self):
        return self.account.name


class IncentiveAccount(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='incentive_ledger'
    )

    def __unicode__(self):
        return self.account.name


class AllowanceName(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


# This is bhatta
class Allowance(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.ForeignKey(
        AllowanceName,
        null=True,
        blank=True,
        related_name="allowances"
    )
    employee_grade = models.ForeignKey(EmployeeGrade)
    account = models.OneToOneField(
        AllowanceAccount,
        null=True,
        blank=True,
        related_name='allowance_account'
    )
    # Any one out of two should be filled
    sum_type = models.CharField(max_length=50, choices=deduct_choice)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
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

    def __unicode__(self):
        if self.sum_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.amount_rate)

    def save(self, *args, **kwargs):
        if not self.account:
            account_name = self.name.name + '-' + str(self.id)
            account_obj = Account.objects.create(name=account_name)
            allowance_account = AllowanceAccount.objects.create(
                account=account_obj,
            )
            self.account = allowance_account
        if self.sum_type == 'AMOUNT':
            self.amount_rate = None
        elif self.sum_type == 'RATE':
            self.amount = None
        if self.payment_cycle is not 'Y':
            self.year_payment_cycle_month = None

        super(Allowance, self).save(*args, **kwargs)

    class Meta:
            unique_together = (("name", "employee_grade"),)


class IncentiveName(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


# This is incentive(for motivation)
class Incentive(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.ForeignKey(
        IncentiveName,
        null=True,
        blank=True,
        related_name='incentives'
    )
    employee_grade = models.ForeignKey(EmployeeGrade)
    account = models.OneToOneField(
        IncentiveAccount,
        null=True,
        blank=True,
        related_name='incentive_account'
    )
    # Any one of the two should be filled
    sum_type = models.CharField(max_length=50, choices=deduct_choice)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
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
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.rate)

    def save(self, *args, **kwargs):
        if not self.account:
            account_name = self.name.name + '-' + str(self.id)
            account_obj = Account.objects.create(name=account_name)
            incentive_account = IncentiveAccount.objects.create(
                account=account_obj,
            )
            self.account = incentive_account
        if self.sum_type == 'AMOUNT':
            self.amount_rate = None
        elif self.sum_type == 'RATE':
            self.amount = None
        if self.payment_cycle is not 'Y':
            self.year_payment_cycle_month = None
        super(Incentive, self).save(*args, **kwargs)

    class Meta:
            unique_together = (("name", "employee_grade"),)


class BranchOffice(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


# These two below should be in setting as many to many
# Imp: Deductin cant be in BAnk Account type and should be one to one with account type
class Deduction(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.CharField(max_length=150)
    # account = models.OneToOneField(
    #     DeductionAccount,
    #     null=True,
    #     blank=True,
    #     related_name='deduction_account'
    # )
    # Below only one out of two should be active
    deduct_type = models.CharField(max_length=50, choices=deduct_choice)
    # deduction_for = models.CharField(max_length=50, choices=deduct_for)
    # Explit acc is only specified when deduction for is explicit_acc
    # explicit_acc = models.ForeignKey(Account, null=True, blank=True)
    # In which type of account to make deduction transaction when deduction for is employee acc
    # in_acc_type = models.ForeignKey(
    #     AccountType,
    #     related_name='in_account_type',
    #     null=True,
    #     blank=True
    # )
    # transact_in = models.CharField(choice=acc_type)
    deduct_in_category = models.ForeignKey(Category, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=150)
    priority = models.IntegerField(unique=True)

    # Whether to include this deduction with temporary employee
    with_temporary_employee = models.BooleanField(default=False)
    # For permanent
    add2_init_salary = models.BooleanField(default=False)

    # If true we can deduct while calculating taxable amount
    is_tax_free = models.BooleanField(default=False)

    is_optional = models.BooleanField(default=False)

    def __unicode__(self):
        if self.deduct_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.amount_rate)


@receiver(post_save, sender=Deduction)
def deduct_in_category_add(sender, instance, created, **kwargs):
    if created:
        instance.deduct_in_category = Category.objects.create(
            name='%s-%d' % (instance.name, instance.id),
            parent_id=ACC_CAT_DEDUCTION_ID
        )
        instance.save()


class Employee(models.Model):
    # Budget code (Functionality to change budget code for employee group)
    budget_code = models.CharField(max_length=100)
    # working_branch = models.CharField(max_length=100)
    # Employee ko section or branch coz he can be in another branch and paid from central
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    marital_statuses = [('M', _('Married')), ('U', _('Unmarried'))]
    employee = models.OneToOneField(User)
    sex = models.CharField(choices=sex_choice, max_length=1)
    marital_status = models.CharField(
        default='U',
        max_length=1,
        choices=marital_statuses
    )
    designation = models.ForeignKey(Designation)
    pan_number = models.CharField(max_length=100)
    working_branch = models.ForeignKey(BranchOffice)
    accounts = models.ManyToManyField(Account, through="EmployeeAccount")
    pf_monthly_deduction_amount = models.FloatField(default=0)
    payment_halt = models.BooleanField(default=False)
    appoint_date = BSDateField(default=today)
    dismiss_date = BSDateField(null=True, blank=True)
    # allowance will be added to salary
    allowances = models.ManyToManyField(AllowanceName, blank=True)
    # incentive will have diff trancation
    incentives = models.ManyToManyField(IncentiveName, blank=True)

    optional_deduction = models.ManyToManyField(
        Deduction,
        blank=True
    )
    # Permanent has extra functionality while deduction from salary
    is_permanent = models.BooleanField(default=False)
    # deductions need to be removed from this table
    # deductions = models.ManyToManyField(Deduction)

    def current_salary_by_month(self, from_date, to_date):
        grade_salary = self.designation.grade.salary_scale
        grade_number = self.designation.grade.grade_number
        grade_rate = self.designation.grade.grade_rate
        salary = 0
        for year, month in get_y_m_tuple_list(from_date, to_date):
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    try:
                        days_worked = date(year, month, 1) - self.appoint_date
                    except:
                        raise TypeError('Internal and external setting mismatch')
                else:
                    if isinstance(self.appoint_date, date):
                        raise TypeError('Internal and external setting mismatch')
                    else:
                        days_worked = date(*bs2ad(date(year, month, 1))) - date(*bs2ad((self.appoint_date)))

            years_worked = days_worked.days / 365
            if years_worked <= grade_number:
                salary += grade_salary + int(years_worked) * grade_rate
            elif years_worked > grade_number:
                salary += grade_salary + grade_number * grade_rate
        return salary

    def current_salary_by_day(self, from_date, to_date):
        if from_date.year == to_date.year and from_date.month == to_date.month:
            salary_pure_months = 0
            lhs_month_salary = 0
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

            rhs_month_salary = self.current_salary_by_month(
                month,
                month
            )

        elif are_side_months(from_date, to_date):
            salary_pure_months = 0
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
            lhs_month_salary = self.current_salary_by_month(
                lhs_month,
                lhs_month
            )
            rhs_month_salary = self.current_salary_by_month(
                rhs_month,
                rhs_month
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
                        to_date_m = date(to_date.year-1, 12, 1)
                    else:
                        to_date_m = date(to_date.year, to_date.month-1, 1)
                    lhs_month = date(from_date.year, from_date.month, 1)
                    rhs_month = date(to_date.year, to_date.month, 1)
                    lhs_days = (from_date_m - from_date).days
                    rhs_days = (to_date - to_date_m).days + 1

                    from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                    to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

                else:
                    if from_date.month == 12:
                        from_date_m = BSDate(from_date.year+1, 1, 1)
                    else:
                        from_date_m = BSDate(from_date.year, from_date.month+1, 1)
                    if to_date.month == 1:
                        to_date_m = BSDate(to_date.year-1, 12, 1)
                    else:
                        to_date_m = BSDate(to_date.year, to_date.month-1, 1)
                    lhs_month = BSDate(from_date.year, from_date.month, 1)
                    rhs_month = BSDate(to_date.year, to_date.month, 1)
                    lhs_days = (from_date_m - from_date).days
                    rhs_days = (to_date - to_date_m).days + 1

                    from_date_month_days = bs[lhs_month.year][lhs_month.month-1]
                    to_date_month_days = bs[rhs_month.year][rhs_month.month-1]

            salary_pure_months = self.current_salary_by_month(
                from_date_m,
                to_date_m
            )
            lhs_month_salary = self.current_salary_by_month(
                lhs_month,
                lhs_month
            )
            rhs_month_salary = self.current_salary_by_month(
                rhs_month,
                rhs_month
            )
        lhs_salary = lhs_month_salary / float(from_date_month_days) * lhs_days
        rhs_salary = rhs_month_salary / float(to_date_month_days) * rhs_days
        salary = salary_pure_months + lhs_salary + rhs_salary
        return salary

        # grade_salary = self.designation.grade.salary_scale
        # grade_number = self.designation.grade.grade_number
        # grade_rate = self.designation.grade.grade_rate
        # salary = 0
        pass

    def has_account(self, account_type):
        for i in self.accounts.all():
            if i.employee_account.other_account_type == account_type:
                return True
        return False

    def __unicode__(self):
        return str(self.employee.full_name)


@receiver(post_save, sender=Employee)
def add_employee_accounts(sender, instance, created, **kwargs):
    if created:
        accounts = []
        # Add salary Account
        salary_account = Account.objects.create(
            name="Salary Account-EID#%d" % instance.id,
            category_id=ACC_CAT_BASIC_SALARY_ID
        )
        salary_emp_account = EmployeeAccount.objects.create(
            account=salary_account,
            employee=instance,
        )
        accounts.append(salary_emp_account)
        # Add deduction accounts (compulsory)
        for deduction in Deduction.objects.filter(is_optional=False):
            deduction_account = Account.objects.create(
                name="Deduction#%d-EID#%d" % (
                    deduction.id,
                    instance.id
                ),
                category=deduction.deduct_in_category
            )
            deduction_emp_account = EmployeeAccount.objects.create(
                account=deduction_account,
                employee=instance,
            )
            accounts.append(deduction_emp_account)
        # Add deduction accounts (compulsory)
        for deduct in instance.optional_deduction.all():
            opt_deduction_account = Account.objects.create(
                name="Deduction#%d-EID#%d" % (
                    deduct.id,
                    instance.id
                ),
                category=deduct.deduct_in_category
            )
            opt_deduction_emp_account = EmployeeAccount.objects.create(
                account=opt_deduction_account,
                employee=instance,
            )
            # accounts.append(opt_deduction_emp_account)
        # instance.accounts.add(*accounts)


class ProTempore(models.Model):
    employee = models.OneToOneField(Employee,
                                    related_name="real_employee_post")
    pro_tempore = models.OneToOneField(Employee,
                                       related_name="virtual_employee_post")
    appoint_date = BSDateField(default=today)
    dismiss_date = BSDateField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    # Employee is permanent o r temporary? 10% PF in permanent
    # Beema(insurance) +200
    # There is also another insurance in Nagarik Lagani kosh()

    #dEDUCTION PART(employee)
    # In  permanent case:
    # 10% x 2 to sanchaikosh
    # Bima ie 200 currently x 2 nagarik lagani kosh(bima)
    # There is also another insurance in Nagarik Lagani kosh().. Person anusar farak rate either in percentage or fixed rate
    # Advance settlement
    # There can also be some other deduction eg in earthquake gov cut it down
    # Social Security tax (1%)
    # Remunuration Tax (income tax)
    # Baki chai either in bank or cash

    # Sabai ko account huncha 


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


class TaxScheme(models.Model):
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


class TaxCalcScheme(models.Model):
    scheme = models.ForeignKey(
        TaxScheme,
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


class DeductionDetail(models.Model):
    deduction = models.ForeignKey(
        Deduction,
        related_name='deduced_amount_detail'
    )
    amount = models.FloatField()


class IncentiveDetail(models.Model):
    incentive = models.ForeignKey(
        IncentiveName,
        related_name='incentive_amount_detail'
    )
    amount = models.FloatField()


class AllowanceDetail(models.Model):
    allowance = models.ForeignKey(
        AllowanceName,
        related_name='allowance_amount_detail'
    )
    amount = models.FloatField()


class PaymentRecord(models.Model):
    paid_employee = models.ForeignKey(Employee)
    paid_from_date = BSDateField()
    paid_to_date = BSDateField()
    absent_days = models.PositiveIntegerField()
    allowance = models.FloatField(null=True, blank=True)
    incentive = models.FloatField(null=True, blank=True)
    pf_deduction_amount = models.PositiveIntegerField(null=True, blank=True)
    deduced_amount = models.FloatField(null=True, blank=True)
    deduction_details = models.ManyToManyField(DeductionDetail, blank=True)
    incentive_details = models.ManyToManyField(IncentiveDetail, blank=True)
    allowance_details = models.ManyToManyField(AllowanceDetail, blank=True)
    income_tax = models.FloatField(null=True, blank=True)
    pro_tempore_amount = models.FloatField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField()
    # Deducted amount fields
    # How much incentive and how much allowance

    def total_present_days(self):
        return self.paid_to_date - self.paid_from_date - self.absent_days

    def __unicode__(self):
        return str(self.id)


class PayrollEntry(models.Model):
    entry_rows = models.ManyToManyField(PaymentRecord)
    branch = models.ForeignKey(BranchOffice, null=True, blank=True)
    is_monthly_payroll = models.BooleanField(default=False)
    entry_datetime = models.DateTimeField(default=timezone.now)
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
        timestamp = ''
        for row in self.entry_rows.all():
            timestamp = "From %s to %s" % (
                str(row.paid_from_date),
                str(row.paid_to_date)
            )
            break
        return '%s-%s-%s-Entry on %s. ' % (
            branch_name,
            typ,
            timestamp,
            str(self.entry_datetime),
        )


def employee_account_validator(acc_id):
    category = Account.objects.get(id=acc_id).category
    if category.id == ACC_CAT_BASIC_SALARY_ID or category.parent.id == ACC_CAT_DEDUCTION_ID:
        pass
    else:
        raise ValidationError(
            _('Account must be of Category BASIC SALARY or DEDUCTION'),
        )


class EmployeeAccount(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='employee_account',
        validators=[employee_account_validator]
    )

    class Meta:
        unique_together = (("employee", "account"),)

    def get_category_name(self):
        return self.account.category.name

    def __unicode__(self):
        return ('%s-acc#%d' % (self.account.category.name, self.account.id))


class CompanyAccount(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='company_account'
    )
    is_salary_giving = models.BooleanField(default=False)


# This stores the pure salary with scale and rate
# One Salary account for each fiscal year should be created
class SalaryAccount(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='salary_account'
    )

# class HrConfig(dbsettings.Group):
#     sk_deduction_rate = models.PositiveIntegerField()
#     maintenance_mode = models.BooleanField(default=False)
#     ** Sanchai Kosh ko percentage
#     ** Tax rate
#     ** Lagu miti of rate
#     ** Absent case

#     def __unicode__(self):
#         return u"hr config"

#     class Meta:
#         verbose_name = "Setup Income Tax Rate"


#  allowance in EmployeeRank
#  Incentive in Employee

# to do
# Maximim provision of grade rate upto 10 times ==> constant or variable
# Manage allowance, Incentive and Tax with  salary
# Think about salary paused
# niyukti **of


# Can employee be django auth user? Yes
# Case of employee as technician##Done

# In case employee is pro-tempore we need to transact his normal salary and extract pro-tempor employee salay, get the difference of their salary and transact differnece seperately
#  Talab rokka
#  When did emloyee start his job
#  
#  
#  Incentive rate employee anusar farak huncha month anusar pani farak parcha
#  Salary advance
#  
#  
#  When Salary increased in middle of the month each day earning shoud be calculated ****
#  
#  
#  
#  Make branch model with code on which employee work
  
  
#  When does increse in scale get active?
#  The day from which the goverment announces it or the day from which the employeer is apponted
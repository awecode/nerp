from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel
from njango.fields import BSDateField

from core.models import FiscalYear, BudgetHead, Donor


@python_2_unicode_compatible
class District(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Office(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name')
    )
    district = models.ForeignKey(
        District,
        verbose_name=_('District')
    )

    def __str__(self):
        return "%s-%s" % (self.name, self.district)


@python_2_unicode_compatible
class Beneficiary(models.Model):
    designation = models.CharField(
        max_length=255,
        verbose_name=_('Designation')
    )
    office = models.CharField(
        max_length=255,
        verbose_name=_('Office')
    )

    def __str__(self):
        return "%s-%s" % (self.designation, self.office)

    class Meta:
        verbose_name_plural = _('Beneficiaries')


@python_2_unicode_compatible
class AuthorityHandover(models.Model):
    AH_TYPE = (
        ('first', _('First')),
        ('addition', _('Addition')),
        ('edited', _('Edited')),
    )
    type = models.CharField(
        max_length=15,
        choices=AH_TYPE
    )
    parent = models.OneToOneField(
        "self",
        related_name="child",
        null=True,
        blank=True
    )
    beneficiary = models.ForeignKey(
        Beneficiary,
        related_name='authority_handovers',
        verbose_name=_('Beneficiary'),
        null=True,
        blank=True
    )
    fiscal_year = models.ForeignKey(
        FiscalYear,
        related_name="authority_handovers",
        verbose_name=_('Fiscal Year')
    )
    budget_head = models.ForeignKey(
        BudgetHead,
        related_name="authority_handovers",
        verbose_name=_('Budget Head')
    )
    priority_code = models.CharField(
        max_length=10,
        verbose_name=_('Priority Code')
    )
    date = BSDateField(
        verbose_name=_('Date')
    )

    def __str__(self):
        return "%s-%s" % (self.date, self.beneficiary)

    # todo below two methods based on changed model
    # todo start
    def individual_fund_sum(self):
        result = self.budget_distributions.aggregate(
            Sum('permitted_budget'),
            Sum('government_fund'),
            Sum('foreign_fund_grant_cash'),
            Sum('foreign_fund_grant_reimbursable'),
            Sum('foreign_fund_grant_direct_payment'),
            Sum('foreign_fund_grant_commodity'),
            Sum('foreign_fund_loan_cash'),
            Sum('foreign_fund_loan_reimbursable'),
            Sum('foreign_fund_loan_direct_payment'),
        )
        return result

    def total_budget(self):
        result = self.individual_fund_sum()
        del result['permitted_budget__sum']
        return sum(result.values())
        # return 787887600075004
        # todo end

    def save(self, *args, **kwargs):
        if not self.parent:
            self.type = 'first'
        super(AuthorityHandover, self).save(*args, **kwargs)



@python_2_unicode_compatible
class ExpenditureHead(models.Model):
    number = models.CharField(
        max_length=20,
        verbose_name=_('Expenditure Head Number')
    )
    name = models.CharField(
        max_length=20,
        verbose_name=_('Expenditure Head Name')
    )

    def __str__(self):
        return "%s-%s" % (self.number, self.name)


@python_2_unicode_compatible
class BudgetDistribution(models.Model):
    authority_handover = models.ForeignKey(AuthorityHandover, related_name='budget_distributions')

    expenditure_head = models.ForeignKey(ExpenditureHead, related_name="budget_distributions", blank=True, null=True)

    permitted_budget = models.PositiveIntegerField(
        verbose_name=_('Permitted Budget'),
        default=0
    )
    government_fund = models.PositiveIntegerField(
        verbose_name=_('Government Fund'),
        default=0
    )

    remarks = models.CharField(
        max_length=255,
        verbose_name=_('Remarks')
    )

    def __str__(self):
        return "%s" % (self.authority_handover)

    def total_fund(self):
        # todo update below calculation based on new model
        return self.government_fund \
               + self.foreign_fund_grant_cash \
               + self.foreign_fund_grant_reimbursable \
               + self.foreign_fund_grant_direct_payment \
               + self.foreign_fund_grant_commodity \
               + self.foreign_fund_grant_commodity \
               + self.foreign_fund_loan_cash \
               + self.foreign_fund_loan_reimbursable \
               + self.foreign_fund_loan_direct_payment


@python_2_unicode_compatible
class ForeignFund(models.Model):
    TYPE_CHOICES = (
        ('grant', 'Grant'),
        ('loan', 'Loan')
    )

    SUB_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('reimbursable', 'Reimbursable'),
        ('direct payment', 'Direct Payment'),
        ('commodity', 'Commodity'),
    )
    budget_distribution = models.ForeignKey(
        BudgetDistribution,
        related_name="foreign_funds",
        verbose_name=_('Budget Distribution')
    )
    donor = models.ForeignKey(
        Donor,
        verbose_name=_('Donor'),
        related_name=_('foreign_funds')
    )
    amount = models.PositiveIntegerField(
        verbose_name=_('Amount')
    )
    type = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES,
        verbose_name=_('Type')
    )
    sub_type = models.CharField(
        max_length=15,
        choices=SUB_TYPE_CHOICES,
        verbose_name=_('Sub Type')
    )

    def __str__(self):
        return "%s-%s-%s" % (self.budget_distribution, self.doner, self.amount)

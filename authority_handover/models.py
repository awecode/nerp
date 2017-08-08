from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel

from core.models import FiscalYear, BudgetHead, Donor


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
    date = models.DateField(
        verbose_name=_('Date')
    )

    def __str__(self):
        return "%s-%s" % (self.date, self.beneficiary)

    def total_budget(self):
        result = self.budget_distributions.aggregate(
            Sum('government_fund'),
            Sum('foreign_fund_grant_cash'),
            Sum('foreign_fund_grant_reimbursable'),
            Sum('foreign_fund_grant_direct_payment'),
            Sum('foreign_fund_grant_commodity'),
            Sum('foreign_fund_loan_cash'),
            Sum('foreign_fund_loan_reimbursable'),
            Sum('foreign_fund_loan_direct_payment'),
        )
        return sum(result.values())
        # return 787887600075004


@python_2_unicode_compatible
class BudgetDistribution(models.Model):
    authority_handover = models.ForeignKey(AuthorityHandover, related_name='budget_distributions')
    expenditure_head_number = models.CharField(
        max_length=20,
        verbose_name=_('Expenditure Head Number')
    )
    expenditure_head_name = models.CharField(
        max_length=20,
        verbose_name=_('Expenditure Head Name')
    )
    permitted_budget = models.PositiveIntegerField(
        verbose_name=_('Permitted Budget'),
        default=0
    )
    government_fund = models.PositiveIntegerField(
        verbose_name=_('Government Fund'),
        default=0
    )

    foreign_fund_grant_cash = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Grant Cash'),
        default=0
    )
    foreign_fund_grant_reimbursable = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Grant Reimbursable'),
        default=0
    )
    foreign_fund_grant_direct_payment = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Grant Direct Payment'),
        default=0
    )
    foreign_fund_grant_commodity = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Grant Commodity'),
        default=0
    )

    foreign_fund_loan_cash = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Loan Cash'),
        default=0
    )
    foreign_fund_loan_reimbursable = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Loan Reimbursable'),
        default=0
    )
    foreign_fund_loan_direct_payment = models.PositiveIntegerField(
        verbose_name=_('Foreign Fund Loan Direct Payment'),
        default=0
    )
    # foreign_fund_loan_commodity = models.PositiveIntegerField(
    #     verbose_name=_('Foreign Fund Loan Commodity')
    # )

    donor = models.ForeignKey(
        Donor,
        verbose_name=_('Donor')
    )

    remarks = models.CharField(
        max_length=255,
        verbose_name=_('Remarks')
    )

    def __str__(self):
        return "%s-%s" % (self.authority_handover, self.expenditure_head_name)

    def total_fund(self):
        return self.government_fund \
               + self.foreign_fund_grant_cash \
               + self.foreign_fund_grant_reimbursable \
               + self.foreign_fund_grant_direct_payment \
               + self.foreign_fund_grant_commodity \
               + self.foreign_fund_grant_commodity \
               + self.foreign_fund_loan_cash \
               + self.foreign_fund_loan_reimbursable \
               + self.foreign_fund_loan_direct_payment

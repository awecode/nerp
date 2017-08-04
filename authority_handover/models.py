from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from core.models import FiscalYear, BudgetHead, Donor


@python_2_unicode_compatible
class AuthorityHandover(models.Model):
    beneficiary_designation = models.CharField(max_length=255)
    beneficiary_office = models.CharField(max_length=255)
    fiscal_year = models.ForeignKey(FiscalYear, related_name="authority_handovers")
    budget_head = models.ForeignKey(BudgetHead, related_name="authority_handovers")
    priority_code = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return "%s-%s-%s" % (self.date, self.beneficiary_designation, self.beneficiary_office)


@python_2_unicode_compatible
class BudgetDistribution(models.Model):
    authority_handover = models.ForeignKey(AuthorityHandover, related_name='budget_distributions')
    expenditure_head_number = models.CharField(max_length=20)
    expenditure_head_name = models.CharField(max_length=20)
    permitted_budget = models.PositiveIntegerField()
    government_fund = models.PositiveIntegerField()

    foreign_fund_grant_cash = models.PositiveIntegerField()
    foreign_fund_grant_reimbursable = models.PositiveIntegerField()
    foreign_fund_grant_direct_payment = models.PositiveIntegerField()
    foreign_fund_grant_commodity = models.PositiveIntegerField()

    foreign_fund_loan_cash = models.PositiveIntegerField()
    foreign_fund_loan_reimbursable = models.PositiveIntegerField()
    foreign_fund_loan_direct_payment = models.PositiveIntegerField()
    foreign_fund_loan_commodity = models.PositiveIntegerField()

    donor = models.ForeignKey(Donor)

    remarks = models.CharField(max_length=255)

    def __str__(self):
        return "%s-%s" % (self.authority_handover, self.expenditure_head_name)


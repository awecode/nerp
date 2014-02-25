from django.db import models

from app.libr import MultiNameModel, transl, ne2en


SOURCES = [('nepal_government', 'Nepal Government'), ('foreign_cash_grant', 'Foreign Cash Grant'),
           ('foreign_compensating_grant', 'Foreign Compensating Grant'), ('foreign_cash_loan', 'Foreign Cash Loan'),
           ('foreign_compensating_loan', 'Foreign Compensating Loan'),
           ('foreign_substantial_aid', 'Foreign Substantial Aid')]


class Account(MultiNameModel):
    # account_page_no = models.IntegerField()
    pass


class Party(MultiNameModel):
    address = models.CharField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    account = models.OneToOneField(Account, related_name='party')

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(name_en=self.name_en, name_ne=self.name_ne)
            account.save()
            self.account = account
        super(Party, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Parties'


class FiscalYear(models.Model):
    years = (
        (2069, "2069/70"),
        (2070, "2070/71"),
        (2071, "2071/72")
    )
    year = models.IntegerField(choices=years, unique=True)

    def __str__(self):
        return str(self.year) + '/' + str(self.year - 1999)


class AppSetting(models.Model):
    app_name = models.CharField(max_length=254)
    fiscal_year = models.ForeignKey(FiscalYear)
    header_for_forms = models.TextField()

    def __str__(self):
        return 'Default Settings ' + str(self.id)


class Employee(MultiNameModel):
    pass

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(name_en=self.name_en, name_ne=self.name_ne)
            account.save()
            self.account = account
        super(Employee, self).save(*args, **kwargs)


class Donor(MultiNameModel):
    pass


class Activity(MultiNameModel):
    no = models.PositiveIntegerField()

    def __str__(self):
        return str(self.no) + ' - ' + self.name

    class Meta:
        verbose_name_plural = 'Activities'


class BudgetHead(MultiNameModel):
    no = models.PositiveIntegerField()

    def get_current_balance(self):
        return BudgetBalance.objects.get(fiscal_year=AppSetting.objects.first(), budget_head=self)

    current_balance = property(get_current_balance)

    def __str__(self):
        return transl(self.no) + ' - ' + self.name

    class Meta:
        verbose_name = 'Budget Head'


class BudgetBalance(models.Model):
    budget_head = models.ForeignKey(BudgetHead, related_name='balance')
    fiscal_year = models.ForeignKey(FiscalYear)
    nepal_government = models.FloatField(default=0)
    foreign_cash_grant = models.FloatField(default=0)
    foreign_compensating_grant = models.FloatField(default=0)
    foreign_cash_loan = models.FloatField(default=0)
    foreign_compensating_loan = models.FloatField(default=0)
    foreign_substantial_aid = models.FloatField(default=0)
    nepal_government_due = models.FloatField(default=0, editable=False)
    foreign_cash_grant_due = models.FloatField(default=0, editable=False)
    foreign_compensating_grant_due = models.FloatField(default=0, editable=False)
    foreign_cash_loan_due = models.FloatField(default=0, editable=False)
    foreign_compensating_loan_due = models.FloatField(default=0, editable=False)
    foreign_substantial_aid_due = models.FloatField(default=0, editable=False)

    def total(self):
        return self.nepal_government + self.foreign_cash_grant + self.foreign_compensating_grant + self.foreign_cash_loan + self.foreign_compensating_loan + self.foreign_substantial_aid

    def __str__(self):
        return self.budget_head.name + ' - ' + str(self.fiscal_year)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.nepal_government_due = self.nepal_government
            self.foreign_cash_grant_due = self.foreign_cash_grant
            self.foreign_compensating_grant_due= self.foreign_compensating_grant
            self.foreign_cash_loan_due = self.foreign_cash_loan
            self.foreign_compensating_loan_due = self.foreign_compensating_loan
            self.foreign_substantial_aid_due = self.foreign_substantial_aid
        super(BudgetBalance, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['budget_head', 'fiscal_year']


class TaxScheme(MultiNameModel):
    percent = models.FloatField()

    def get_multiplier(self):
        return self.percent / 100

    multiplier = property(get_multiplier)

    def __str__(self):
        return self.name + ' (' + str(self.percent) + '%)'
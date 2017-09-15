from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from njango.fields import BSDateField, today

from app.utils.helpers import model_exists_in_db
from core.models import Currency, FiscalYear, validate_in_fy, Donor, BudgetHead
from account.models import Account, Party

IMPREST_TRANSACTION_TYPES = (('initial_deposit', 'Initial Deposit'), ('gon_fund_transfer', 'GON Fund Transfer'),
                             ('replenishment_received', 'Replenishment Received'),
                             ('payment', 'Payment'), ('liquidation', 'Liquidation'))

AID_TYPES = (('loan', 'Loan'), ('grant', 'Grant'))

DISBURSEMENT_METHOD = (
    ('reimbursement', 'Reimbursement'), ('replenishment', 'Replenishment'), ('liquidation', 'Liquidation'),
    ('direct_payment', 'Direct Payment'))

DEFAULT_LEDGERS = [
    'Initial Deposit',
    'Ka-7-15',
    'Ka-7-17',
    'Replenishments',
]


class Project(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def get_imprest_ledger(self, fy=None):
        return self.get_for_fy(fy).imprest_ledger

    def get_or_create_for_fy(self, fy=None):
        if not fy:
            fy = FiscalYear.get()
        elif type(fy) in [int, str]:
            fy = FiscalYear.get(fy)

        return ProjectFy.objects.get_or_create(project=self, fy=fy)

    @property
    def project_fy(self):
        return self.get_for_fy()

    def get_for_fy(self, fy=None):
        project_fy, created = self.get_or_create_for_fy()
        return project_fy

    def __str__(self):
        return self.name


class ProjectFy(models.Model):
    project = models.ForeignKey(Project)
    fy = models.ForeignKey(FiscalYear)
    imprest_ledger = models.ForeignKey(Account, related_name='imprest_for')
    initial_deposit = models.ForeignKey(Account, related_name='deposit_for')
    replenishments = models.ForeignKey(Account, related_name='replenishments_for')
    additional_advances = models.ForeignKey(Account, related_name='additional_advances_for')

    def __str__(self):
        return str(self.project) + ' - ' + str(self.fy)

    def save(self, *args, **kwargs):
        if not self.imprest_ledger_id:
            self.imprest_ledger = Account.objects.create(name='Imprest Ledger (' + str(self.project.name) + ')',
                                                         fy=self.fy)
        if not self.initial_deposit_id:
            self.initial_deposit = Account.objects.create(name='Initial Deposit (' + str(self.project.name) + ')',
                                                          fy=self.fy)
        if not self.replenishments_id:
            self.replenishments = Account.objects.create(name='Replenishments (' + str(self.project.name) + ')', fy=self.fy)
        if not self.additional_advances_id:
            self.additional_advances = Account.objects.create(name='Additional Advances (' + str(self.project.name) + ')',
                                                              fy=self.fy)
        super(ProjectFy, self).save(*args, **kwargs)

    def get_ledgers(self):
        self_ledgers = [self.imprest_ledger, self.initial_deposit, self.replenishments, self.additional_advances]
        party_ledgers = [party.account for party in Party.objects.all()]
        return self_ledgers + party_ledgers

    def dr_ledgers(self):
        party_ledgers = [party.account for party in Party.objects.all()]
        return [self.imprest_ledger, Account.objects.filter(name='Ka-7-15', fy=self.fy).first(),
                Account.objects.filter(name='Ka-7-17', fy=self.fy).first()] + party_ledgers

    def cr_ledgers(self):
        return [self.imprest_ledger, self.initial_deposit, self.replenishments, self.additional_advances]

    class Meta:
        unique_together = ('project', 'fy')
        verbose_name = 'Project Fiscal Year'
        verbose_name_plural = 'Project Fiscal Years'


@receiver(post_save, sender=Project)
def on_project_add(sender, instance, created, **kwargs):
    if created:
        fys = FiscalYear.objects.all()
        for fy in fys:
            instance.get_or_create_for_fy(fy)


@receiver(post_save, sender=FiscalYear)
def on_fy_add(sender, instance, created, **kwargs):
    if created and model_exists_in_db(Project):
        projects = Project.objects.filter(active=True)
        for project in projects:
            project.get_or_create_for_fy(instance)


class Aid(models.Model):
    donor = models.ForeignKey(Donor)
    type = models.CharField(choices=AID_TYPES, max_length=10)
    key = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    project = models.ForeignKey(Project)

    def __str__(self):
        return str(self.donor) + ' ' + str(self.get_type_display()) + ' ' + self.key


class Signatory(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    default = models.BooleanField(default=False, verbose_name='Required to sign on all notes?')
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Signatories'


class ImprestTransaction(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, choices=IMPREST_TRANSACTION_TYPES)
    date = BSDateField(null=True, blank=True, default=today, validators=[validate_in_fy])
    date_of_payment = BSDateField(null=True, blank=True, default=today, validators=[validate_in_fy])
    wa_no = models.CharField(max_length=10, verbose_name='Withdrawal Application No.', null=True, blank=True)
    # ref = models.CharField(max_length=10, verbose_name='Reference', null=True, blank=True)
    amount_nrs = models.FloatField(blank=True, null=True)
    amount_usd = models.FloatField(blank=True, null=True)
    # currency = models.ForeignKey(Currency)
    # description = models.TextField(null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True)
    project_fy = models.ForeignKey(ProjectFy)

    def __str__(self):
        return self.name or self.get_type_display()


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    gon_funded = models.BooleanField(default=False, verbose_name='GON Funded?')
    order = models.PositiveIntegerField(default=0)
    project = models.ForeignKey(Project)

    def __str__(self):
        st = self.name
        if self.code:
            st = st + ' - ' + self.code
        return st

    def get_absolute_url(self):
        #     TODO after CRUD
        return '# TODO'

    class Meta(object):
        ordering = ('order',)
        verbose_name_plural = 'Expense Categories'


class Expense(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    category = models.ManyToManyField(ExpenseCategory, blank=True)
    enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    project = models.ForeignKey(Project)

    def __str__(self):
        st = self.name
        if self.code:
            st = st + ' - ' + self.code
        return st

    class Meta(object):
        ordering = ('order',)


class ExpenseRow(models.Model):
    category = models.ForeignKey(ExpenseCategory)
    expense = models.ForeignKey(Expense)
    amount = models.FloatField()
    project_fy = models.ForeignKey(ProjectFy)

    def __str__(self):
        return str(self.fy) + '-' + str(self.category) + ' - ' + str(self.expense) + ' : ' + str(self.amount)


class BudgetAllocationItem(models.Model):
    budget_head = models.ForeignKey(BudgetHead)
    aid = models.ForeignKey(Aid, blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    project_fy = models.ForeignKey(ProjectFy)

    def __str__(self):
        aid = 'GON'
        if self.aid:
            aid = str(self.aid)
        return str(self.budget_head) + ' ' + aid + ' ' + str(self.amount)


class BudgetReleaseItem(models.Model):
    budget_head = models.ForeignKey(BudgetHead)
    aid = models.ForeignKey(Aid, blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    project_fy = models.ForeignKey(ProjectFy)

    def __str__(self):
        aid = 'GON'
        if self.aid:
            aid = str(self.aid)
        return str(self.budget_head) + ' ' + aid + ' ' + str(self.amount)


class Expenditure(models.Model):
    budget_head = models.ForeignKey(BudgetHead)
    aid = models.ForeignKey(Aid, blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    project_fy = models.ForeignKey(ProjectFy)

    def __str__(self):
        aid = 'GON'
        if self.aid:
            aid = str(self.aid)
        return str(self.budget_head) + ' ' + aid + ' ' + str(self.amount)


class ImprestJournalVoucher(models.Model):
    voucher_no = models.PositiveIntegerField()
    # date = BSDateField(default=today, validators=[validate_in_fy])
    date = models.DateField()
    dr = models.ForeignKey(Account, related_name='debiting_vouchers')
    cr = models.ForeignKey(Account, related_name='crediting_vouchers')
    amount_nrs = models.FloatField(blank=True, null=True)
    amount_usd = models.FloatField(blank=True, null=True)
    exchange_rate = models.FloatField(blank=True, null=True)
    wa_no = models.CharField(max_length=10, blank=True, null=True)
    project_fy = models.ForeignKey(ProjectFy)

    def is_dr(self):
        if (self.dr.name.startswith('Imprest Ledger')):
            return True

    def is_cr(self):
        if (self.cr.name.startswith('Imprest Ledger')):
            return True

    def against(self):
        if self.is_dr():
            return self.cr
        elif self.is_cr():
            return self.dr

    def __str__(self):
        return str(self.voucher_no)


class Reimbursement(models.Model):
    date = BSDateField(null=True, blank=True, default=today, validators=[validate_in_fy])
    bank_voucher_no = models.PositiveIntegerField(blank=True, null=True)
    wa_no = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    project_fy = models.ForeignKey(ProjectFy)

    def __str__(self):
        return str(self.bank_voucher_no) + ':' + str(self.wa_no)


class DisbursementDetail(models.Model):
    wa_no = models.PositiveIntegerField(blank=True, null=True)
    aid = models.ForeignKey(Aid)
    requested_date = BSDateField(null=True, blank=True, default=today, validators=[validate_in_fy])
    disbursement_method = models.CharField(max_length=255, choices=DISBURSEMENT_METHOD)
    project_fy = models.ForeignKey(ProjectFy)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.aid) + ' - ' + self.disbursement_method


class DisbursementParticulars(models.Model):
    expense_category = models.ForeignKey(ExpenseCategory)
    request_nrs = models.PositiveIntegerField(blank=True, null=True)
    request_usd = models.PositiveIntegerField(blank=True, null=True)
    request_sdr = models.PositiveIntegerField(blank=True, null=True)
    response_nrs = models.PositiveIntegerField(blank=True, null=True)
    response_usd = models.PositiveIntegerField(blank=True, null=True)
    response_sdr = models.PositiveIntegerField(blank=True, null=True)
    with_held_nrs = models.PositiveIntegerField(blank=True, null=True)
    with_held_usd = models.PositiveIntegerField(blank=True, null=True)
    with_held_sdr = models.PositiveIntegerField(blank=True, null=True)
    disbursement_detail = models.ForeignKey(DisbursementDetail, related_name="rows")

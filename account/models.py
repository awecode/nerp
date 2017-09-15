import datetime

from django.core.urlresolvers import reverse
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models import Q

from app.utils.helpers import zero_for_none, none_for_zero, model_exists_in_db
from core.models import FiscalYear, Donor, Activity, BudgetHead, TaxScheme
from django.db.models import F


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    # company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name

    def get_data(self):
        node = Node(self)
        return node.get_data()

    def get_descendant_ledgers(self):
        ledgers = self.accounts.all()
        for descendant in self.get_descendants():
            ledgers = ledgers | descendant.accounts.all()
        return ledgers

    class Meta:
        verbose_name_plural = u'Categories'


class Account(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    # company = models.ForeignKey(Company)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    category = models.ForeignKey(Category, related_name='accounts', blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    opening_dr = models.FloatField(default=0)
    opening_cr = models.FloatField(default=0)
    fy = models.ForeignKey(FiscalYear, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        # return '/ledger/' + str(self.id)
        return reverse('view_ledger', kwargs={'pk': self.pk})

    # def get_last_day_last_transaction(self):
    #     transactions = Transaction.objects.filter(account=self, date__lt=date.today()).order_by('-id', '-date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0]
    #
    # def get_last_transaction_before(self, before_date):
    #     transactions = Transaction.objects.filter(account=self, date__lt=before_date).order_by('-id', '-date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0]
    #
    @property
    def balance(self):
        return self.get_balance()

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def get_day_opening_dr(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return self.current_dr

    def get_day_opening_cr(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return self.current_cr

    def get_day_opening(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return zero_for_none(transactions[0].current_dr) - zero_for_none(transactions[0].current_cr)
        return self.opening_dr - self.opening_cr

    # day_opening_dr = property(get_day_opening_dr)
    # day_opening_cr = property(get_day_opening_cr)
    #
    # day_opening = property(get_day_opening)

    def add_category(self, category):
        # all_categories = self.get_all_categories()
        category_instance, created = Category.objects.get_or_create(name=category, company=self.company)
        # self.categories.add(category_instance)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    def get_cr_amount(self, day):
        # journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return 0

    def get_dr_amount(self, day):
        # journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return 0

    def save(self, *args, **kwargs):
        queryset = Account.objects.all()
        original_name = self.name
        nxt = 2
        if not self.pk:
            while queryset.filter(**{'name': self.name, 'fy': self.fy}):
                self.name = original_name
                end = '%s%s' % ('-', nxt)
                if len(self.name) + len(end) > 100:
                    self.name = self.name[:100 - len(end)]
                self.name = '%s%s' % (self.name, end)
                nxt += 1
        return super(Account, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'fy')
        ordering = ('order',)


class JournalVoucher(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear)
    voucher_no = models.PositiveIntegerField()
    date = models.DateField()


class JournalVoucherRow(models.Model):
    account = models.ForeignKey(Account)
    dr_amount = models.PositiveIntegerField(blank=True, null=True)
    cr_amount = models.PositiveIntegerField(blank=True, null=True)


class Receipt(models.Model):
    date = models.DateField()
    no = models.PositiveIntegerField()
    fiscal_year = models.ForeignKey(FiscalYear)


class ReceiptRow(models.Model):
    sn = models.PositiveIntegerField()
    budget_head = models.ForeignKey(BudgetHead)
    account = models.ForeignKey(Account)
    invoice_no = models.PositiveIntegerField(blank=True, null=True)
    # amount = models.FloatField()
    vattable = models.BooleanField(default=False)

    nepal_government = models.FloatField(blank=True, null=True)
    foreign_cash_grant = models.FloatField(blank=True, null=True)
    foreign_compensating_grant = models.FloatField(blank=True, null=True)
    foreign_cash_loan = models.FloatField(blank=True, null=True)
    foreign_compensating_loan = models.FloatField(blank=True, null=True)
    foreign_substantial_aid = models.FloatField(blank=True, null=True)

    donor = models.ForeignKey(Donor, blank=True, null=True)

    advanced = models.FloatField(blank=True, null=True)
    advanced_settlement = models.FloatField(blank=True, null=True)
    cash_returned = models.FloatField(blank=True, null=True)

    tax_scheme = models.ForeignKey(TaxScheme)
    activity = models.ForeignKey(Activity, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)

    receipt = models.ForeignKey(Receipt, related_name='rows')


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    source = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.object_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'Journal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


def alter(account, date, dr_difference, cr_difference):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))


def set_transactions(submodel, date, *args):
    if isinstance(date, unicode):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), object_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(zero_for_none(arg[2]))
                transaction.cr_amount = None
                transaction.account.current_dr = none_for_zero(
                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
                alter(arg[1], date, float(arg[2]), 0)
            if arg[0] == 'cr':
                # import ipdb
                # ipdb.set_trace()
                transaction.cr_amount = float(zero_for_none(arg[2]))
                transaction.dr_amount = None
                transaction.account.current_cr = none_for_zero(
                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
                alter(arg[1], date, 0, float(arg[2]))
            transaction.current_dr = none_for_zero(
                zero_for_none(transaction.account.get_dr_amount(date + datetime.timedelta(days=1)))
                + zero_for_none(transaction.dr_amount))
            transaction.current_cr = none_for_zero(
                zero_for_none(transaction.account.get_cr_amount(date + datetime.timedelta(days=1)))
                + zero_for_none(transaction.cr_amount))
        else:
            transaction = matches[0]
            transaction.account = arg[1]

            # cancel out existing dr_amount and cr_amount from current_dr and current_cr
            # if transaction.dr_amount:
            #     transaction.current_dr -= transaction.dr_amount
            #     transaction.account.current_dr -= transaction.dr_amount
            #
            # if transaction.cr_amount:
            #     transaction.current_cr -= transaction.cr_amount
            #     transaction.account.current_cr -= transaction.cr_amount

            # save new dr_amount and add it to current_dr/cr
            if arg[0] == 'dr':
                # import ipdb
                # ipdb.set_trace()
                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
            else:
                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None

            transaction.current_dr = none_for_zero(zero_for_none(transaction.current_dr) + dr_difference)
            transaction.current_cr = none_for_zero(zero_for_none(transaction.current_cr) + cr_difference)
            transaction.account.current_dr = none_for_zero(
                zero_for_none(transaction.account.current_dr) + dr_difference)
            transaction.account.current_cr = none_for_zero(
                zero_for_none(transaction.account.current_cr) + cr_difference)

        # the following code lies outside if,else block, inside for loop
        transaction.account.save()
        try:
            journal_entry.transactions.add(transaction, bulk=False)
        except TypeError:  # for Django <1.9
            journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            try:
                JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                         model_id=instance.id).delete()
            except:
                pass
            instance.delete()


class Node(object):
    def __init__(self, model, parent=None, depth=0):
        self.children = []
        self.model = model
        self.name = self.model.name
        self.type = self.model.__class__.__name__
        self.dr = 0
        self.cr = 0
        self.url = None
        self.depth = depth
        self.parent = parent
        if self.type == 'Category':
            for child in self.model.children.all():
                self.add_child(Node(child, parent=self, depth=self.depth + 1))
            for account in self.model.accounts.all():
                self.add_child(Node(account, parent=self, depth=self.depth + 1))
        if self.type == 'Account':
            self.dr = self.model.current, 'company_dr or 0'
            self.cr = self.model.current_cr or 0
            self.url = self.model.get_absolute_url()
        if self.parent:
            self.parent.dr += self.dr
            self.parent.cr += self.cr

    def add_child(self, obj):
        self.children.append(obj.get_data())

    def get_data(self):
        data = {
            'name': self.name,
            'type': self.type,
            'dr': self.dr,
            'cr': self.cr,
            'nodes': self.children,
            'depth': self.depth,
            'url': self.url,
        }
        return data

    def __str__(self):
        return self.name


# @receiver(post_save, sender=FiscalYear)
# def fy_add(sender, instance, created, **kwargs):
#     if created:
#         Account.objects.create(name='Ka-7-15', fy=instance)
#         Account.objects.create(name='Ka-7-17', fy=instance)


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr -= transaction.cr_amount

    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()


from django.db.models.signals import post_save


@receiver(post_save, sender=FiscalYear)
def fy_add(sender, instance, created, **kwargs):

    from hr.models import EmployeeAccount
    if created and model_exists_in_db(Account) and model_exists_in_db(EmployeeAccount):
        employee_accounts = Account.objects.filter(~Q(employee_account=None))
        for emp_acc in employee_accounts:
            EmployeeAccount.objects.get_or_create(
                employee=emp_acc.employee_account.employee,
                account=Account.objects.get_or_create(
                    name=emp_acc.name,
                    category=emp_acc.category,
                    fy=instance
                )[0]
            )

        non_employee_accounts = Account.objects.filter(employee_account=None)
        for non_emp_acc in non_employee_accounts:
            Account.objects.get_or_create(
                name=non_emp_acc.name,
                category=non_emp_acc.category,
                fy=instance
            )


class Party(models.Model):
    name = models.CharField(max_length=254, verbose_name=_('Name'))
    address = models.CharField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    account = models.OneToOneField(Account, related_name='party')

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(name=self.name)
            account.save()
            self.account = account
        super(Party, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Parties')

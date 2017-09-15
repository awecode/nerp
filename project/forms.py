from django.core.urlresolvers import reverse_lazy
from django import forms

from app.utils.forms import HTML5BootstrapModelForm, KOModelForm
from models import Aid, Project, ExpenseCategory, Expense, ImprestJournalVoucher, Reimbursement, DisbursementDetail


class AidForm(HTML5BootstrapModelForm):
    class Meta:
        model = Aid
        exclude = ('project',)
        widgets = {
            'donor': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('donor_add')}),
            'project': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('project_add')}),
            'type': forms.Select(attrs={'class': 'selectize'}),
        }


class ProjectForm(HTML5BootstrapModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class ExpenseCategoryForm(HTML5BootstrapModelForm):
    class Meta:
        model = ExpenseCategory
        exclude = ('project',)


class ExpenseForm(KOModelForm):
    class Meta:
        model = Expense
        exclude = ('project',)
        widgets = {
            'category': forms.SelectMultiple(
                attrs={'class': 'selectize'}),
        }


class ImprestJVForm(KOModelForm):
    class Meta:
        model = ImprestJournalVoucher
        exclude = ('project_fy',)


class ReimbursementForm(HTML5BootstrapModelForm):
    class Meta:
        model = Reimbursement
        exclude = ('project_fy',)


class DisbursementDetailForm(HTML5BootstrapModelForm):
    class Meta:
        model = DisbursementDetail
        exclude = ('project_fy',)
        widgets = {
            'aid': forms.Select(attrs={'class': 'selectize'}),
            'disbursement_method': forms.Select(attrs={'class': 'selectize'}),
        }

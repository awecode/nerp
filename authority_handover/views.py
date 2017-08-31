import collections

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, TemplateView

from app.utils.mixins import GroupRequiredMixin, ListView, CreateView, UpdateView, DeleteView, FormsetViewMixin
from authority_handover.filters import AuthorityHandoverFilter
from authority_handover.forms import AuthorityHandoverForm, BudgetDistributionForm
from authority_handover.models import AuthorityHandover, BudgetDistribution, Beneficiary
from authority_handover.serializers import BeneficiaryChoiceSerializer, AuthorityHandoverChoiceSerializer
from core.models import Donor, BudgetHead, FiscalYear
from core.serializers import DonorChoiceSerializer, BudgetHeadChoiceSerializer, FiscalYearChoiceSerializer


class AuthorityHandoverView(GroupRequiredMixin):
    model = AuthorityHandover
    form_class = AuthorityHandoverForm

    group_required = []
    success_url = reverse_lazy('authority-handover-list')


class AuthorityHandoverListView(AuthorityHandoverView, ListView):
    search_fields = []
    search_exact_fields = []
    filter_set = AuthorityHandoverFilter


class AuthorityHandoverDeleteView(AuthorityHandoverView, DeleteView):
    group_required = []


class AuthorityHandoverDetailView(AuthorityHandoverView, DetailView):
    def get_context_data(self, **kwargs):
        context = super(AuthorityHandoverDetailView, self).get_context_data()
        detail_object = self.get_object()
        context['previous_handovers'] = AuthorityHandover.objects.filter(
            date__lt=detail_object.date).order_by('-id')
        return context


class AuthorityHandoverCreate(TemplateView):
    template_name = "authority_handover/authorityhandover_form.html"

    def get_context_data(self, **kwargs):
        context = {}

        donor_choices = DonorChoiceSerializer(
            Donor.objects.all(),
            many=True
        ).data
        budget_head_choices = BudgetHeadChoiceSerializer(
            BudgetHead.objects.all(),
            many=True
        ).data

        fiscal_year_choices = FiscalYearChoiceSerializer(
            FiscalYear.objects.all(),
            many=True
        ).data

        beneficiary_choices = BeneficiaryChoiceSerializer(
            Beneficiary.objects.all(),
            many=True
        ).data

        authority_handover_choices = AuthorityHandoverChoiceSerializer(
            AuthorityHandover.objects.all(),
            many=True
        ).data
        status = {
            'is_loading': False,
            'error': None,
        }
        context['init_actions'] = [
            {
                'type': 'LOAD_CHOICES',
                'app_name': 'authority_handover',
                'model_name': 'authority_handover',
                'data': authority_handover_choices,
                'status': status
            },
            {
                'type': 'LOAD_CHOICES',
                'app_name': 'authority_handover',
                'model_name': 'beneficiary',
                'data': beneficiary_choices,
                'status': status
            },
            {
                'type': 'LOAD_CHOICES',
                'app_name': 'core',
                'model_name': 'fiscal_year',
                'data': fiscal_year_choices,
                'status': status
            },
            {
                'type': 'LOAD_CHOICES',
                'app_name': 'core',
                'model_name': 'budget_head',
                'data': budget_head_choices,
                'status': status
            },
            {
                'type': 'LOAD_CHOICES',
                'app_name': 'core',
                'model_name': 'donor',
                'data': donor_choices,
                'status': status
            },
        ]

        return context

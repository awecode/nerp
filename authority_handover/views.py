from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, TemplateView

from app.utils.mixins import GroupRequiredMixin, ListView, CreateView, UpdateView, DeleteView, FormsetViewMixin
from authority_handover.filters import AuthorityHandoverFilter
from authority_handover.forms import AuthorityHandoverForm, BudgetDistributionForm
from authority_handover.models import AuthorityHandover, BudgetDistribution


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


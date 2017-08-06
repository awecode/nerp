from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from app.utils.mixins import GroupRequiredMixin, ListView, CreateView, UpdateView, DeleteView, FormsetViewMixin
from authority_handover.filters import AuthorityHandoverFilter
from authority_handover.forms import AuthorityHandoverForm, BudgetDistributionForm
from authority_handover.models import AuthorityHandover, BudgetDistribution


class AuthorityHandoverView(GroupRequiredMixin):
    model = AuthorityHandover
    form_class = AuthorityHandoverForm

    child_model = BudgetDistribution
    child_form_class = BudgetDistributionForm
    group_required = []


class AuthorityHandoverListView(AuthorityHandoverView, ListView):
    search_fields = []
    search_exact_fields = []
    filter_set = AuthorityHandoverFilter


class AuthorityHandoverCreateView(AuthorityHandoverView, FormsetViewMixin, CreateView):
    pass


class AuthorityHandoverUpdateView(AuthorityHandoverView, FormsetViewMixin, UpdateView):
    pass


class AuthorityHandoverDeleteView(AuthorityHandoverView, DeleteView):
    group_required = []


class AuthorityHandoverDetailView(AuthorityHandoverView, DetailView):
    pass

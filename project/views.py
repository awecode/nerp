import json

from django.db.models import Q
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView as BaseCreateView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

from account.models import Account
from core.serializers import BudgetSerializer
from account.serializers import AccountSerializer
from app.utils.helpers import save_model, invalid, empty_to_none
from core.models import BudgetHead
from inventory.models import delete_rows
from models import Aid, ProjectFy, ImprestJournalVoucher, BudgetAllocationItem, BudgetReleaseItem, Expenditure, \
    Reimbursement, DisbursementDetail, DisbursementParticulars
from project.forms import AidForm, ProjectForm, ExpenseCategoryForm, ExpenseForm, ImprestJVForm, ReimbursementForm, \
    DisbursementDetailForm
from models import ExpenseRow, ExpenseCategory, Expense, Project
from serializers import ExpenseRowSerializer, ExpenseCategorySerializer, \
    ExpenseSerializer, AidSerializer, BaseStatementSerializer, ImprestJVSerializer, DisbursementDetailSerializer
from app.utils.mixins import AjaxableResponseMixin, UpdateView, DeleteView, json_from_object


class ProjectCreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Add')
        if self.request.is_ajax():
            base_template = 'modal.html'
        else:
            base_template = '_project_base.html'
        context['base_template'] = base_template
        return context


class ProjectFYView(object):
    def dispatch(self, request, *args, **kwargs):
        self.project_fy = get_object_or_404(ProjectFy, pk=self.kwargs.get('project_fy_id'))
        self.project = self.project_fy.project
        self.fy = self.project_fy.fy
        return super(ProjectFYView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project_fy = self.project_fy
        return super(ProjectFYView, self).form_valid(form)

    def get_queryset(self):
        qs = super(ProjectFYView, self).get_queryset()
        qs = qs.filter(project_fy_id=self.project_fy.id)
        return qs

    def get_context_data(self, **kwargs):
        context_data = super(ProjectFYView, self).get_context_data(**kwargs)
        context_data['project_fy'] = self.project_fy
        context_data['project'] = self.project
        context_data['fy'] = self.fy
        if 'data' in context_data:
            context_data['data']['project_fy_id'] = self.project_fy.id
            context_data['data']['fy_id'] = self.fy.id
            context_data['data']['project_id'] = self.project.id
        return context_data


def index(request):
    projects = Project.objects.filter(active=True)
    return render(request, 'project_index.html', {'projects': projects})


# def imprest_ledger(request, project_id):
#     project = Project.objects.get(pk=project_id)
#     context = {
#         'fy': FiscalYear.get(),
#         'project': project,
#     }
#     return render(request, 'imprest_ledger.html', context)
# 
# 
# class ImprestLedger(ProjectFYView, ListView):
#     model = ImprestTransaction
#     template_name = 'imprest_ledger.html'
#     fy = None
# 
#     def get_context_data(self, **kwargs):
#         context_data = super(ImprestLedger, self).get_context_data(**kwargs)
#         context_data['data'] = {
#             'rows': ImprestTransactionSerializer(context_data['object_list'], many=True).data,
#         }
#         return context_data
# 
#     def get_queryset(self):
#         qs = super(ImprestLedger, self).get_queryset()
#         qs = qs.filter(fy=self.get_fy())
#         return qs
# 
# 
# @login_required
# def save_imprest_ledger(request):
#     params = json.loads(request.body)
#     dct = {'rows': {}}
#     model = ImprestTransaction
#     fy_id = params.get('fy_id')
#     try:
#         for ind, row in enumerate(params.get('table_view').get('rows')):
#             if invalid(row, ['date']):
#                 continue
#             values = {'date': row.get('date', ''),
#                       'name': row.get('name'),
#                       'type': row.get('type'),
#                       'date_of_payment': row.get('date_of_payment', ''),
#                       'wa_no': row.get('wa_no'),
#                       'amount_nrs': row.get('amount_nrs', None),
#                       'amount_usd': row.get('amount_usd', None),
#                       'exchange_rate': row.get('exchange_rate', None),
#                       'fy_id': fy_id
#                       }
#             submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#             if not created:
#                 submodel = save_model(submodel, values)
#             dct['rows'][ind] = submodel.id
#     except Exception as e:
#         if hasattr(e, 'messages'):
#             dct['error_message'] = '; '.join(e.messages)
#         elif str(e) != '':
#             dct['error_message'] = str(e)
#         else:
#             dct['error_message'] = 'Error in form data!'
#     delete_rows(params.get('table_view').get('deleted_rows'), model)
#     return JsonResponse(dct)


class Application(ProjectFYView, ListView):
    model = ExpenseRow
    template_name = 'application.html'

    def get_context_data(self, **kwargs):
        context_data = super(Application, self).get_context_data(**kwargs)
        categories = ExpenseCategory.objects.filter(enabled=True, project=self.project)
        expenses = Expense.objects.filter(enabled=True, project=self.project)
        context_data['data'] = {
            'rows': ExpenseRowSerializer(context_data['object_list'], many=True).data,
            'categories': ExpenseCategorySerializer(categories, many=True).data,
            'expenses': ExpenseSerializer(expenses, many=True).data,
        }
        return context_data


@login_required
def save_application(request):
    params = json.loads(request.body)
    dct = {'categories': {}}
    model = ExpenseRow
    project_fy_id = params.get('project_fy_id')
    try:
        for cat_index, category in enumerate(params.get('categories')):
            dct['categories'][cat_index] = {'rows': {}}
            for ind, row in enumerate(category.get('rows')):
                if invalid(row, ['category_id', 'expense_id', 'amount']):
                    continue
                values = {'category_id': row.get('category_id'),
                          'expense_id': row.get('expense_id'),
                          'amount': row.get('amount'),
                          'project_fy_id': project_fy_id,
                          }
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['categories'][cat_index]['rows'][ind] = submodel.id
            delete_rows(category.get('deleted_rows'), model)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    # delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)


class ProjectMixin(object):
    def get_queryset(self):
        queryset = super(ProjectMixin, self).get_queryset()
        if 'project_id' in self.kwargs:
            queryset = self.model.objects.filter(project_id=self.kwargs['project_id'])
        return queryset

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_id'])
        super(ProjectMixin, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(ProjectMixin, self).post(request, *args, **kwargs)
        if self.request.is_ajax():
            return json_from_object(self.object)
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'project_id': self.kwargs['project_id']}))

    def get_context_data(self, **kwargs):
        context_data = super(ProjectMixin, self).get_context_data(**kwargs)
        context_data['project'] = Project.objects.get(pk=self.kwargs.get('project_id'))
        return context_data


class AidView(ProjectMixin):
    model = Aid
    success_url = 'aid_list'
    form_class = AidForm


class AidList(AidView, ListView):
    pass


class AidCreate(AjaxableResponseMixin, AidView, ProjectCreateView):
    pass


class AidUpdate(AidView, UpdateView):
    pass


class AidDelete(AidView, DeleteView):
    pass


class ProjectAppView(object):
    model = Project
    success_url = reverse_lazy('project_list')
    form_class = ProjectForm


class ProjectList(ProjectAppView, ListView):
    pass


class ProjectCreate(AjaxableResponseMixin, ProjectAppView, ProjectCreateView):
    pass


class ProjectUpdate(ProjectAppView, UpdateView):
    pass


class ProjectDelete(ProjectAppView, DeleteView):
    pass


class ExpenseCategoryView(ProjectMixin):
    model = ExpenseCategory
    success_url = 'expense_category_list'
    form_class = ExpenseCategoryForm


class ExpenseCategoryList(ExpenseCategoryView, ListView):
    pass


class ExpenseCategoryCreate(AjaxableResponseMixin, ExpenseCategoryView, ProjectCreateView):
    pass


class ExpenseCategoryUpdate(ExpenseCategoryView, UpdateView):
    pass


class ExpenseCategoryDelete(ExpenseCategoryView, DeleteView):
    pass


class ExpenseView(ProjectMixin):
    model = Expense
    success_url = 'expense_list'
    form_class = ExpenseForm

    def get_context_data(self, **kwargs):
        context_data = super(ExpenseView, self).get_context_data(**kwargs)
        if 'form' in context_data:
            project_id = context_data['project'].id
            form = context_data['form']
            form.fields['category'].queryset = ExpenseCategory.objects.filter(project_id=project_id)
        return context_data


class ExpenseList(ExpenseView, ListView):
    pass


class ExpenseCreate(AjaxableResponseMixin, ExpenseView, ProjectCreateView):
    pass


class ExpenseUpdate(ExpenseView, UpdateView):
    pass


class ExpenseDelete(ExpenseView, DeleteView):
    pass


class BaseStatement(object):
    def get_context_data(self, **kwargs):
        context_data = super(BaseStatement, self).get_context_data(**kwargs)
        budget_heads = BudgetHead.objects.all()
        aids = Aid.objects.filter(active=True, project=self.project)
        context_data['data'] = {
            'rows': BaseStatementSerializer(context_data['object_list'], many=True).data,
            'budget_heads': BudgetSerializer(budget_heads, many=True).data,
            'aids': AidSerializer(aids, many=True).data,
        }
        return context_data


def base_save(request, model):
    params = json.loads(request.body)
    project_fy_id = params.get('project_fy_id')
    dct = {'rows': {}}
    try:
        table_view = ('budget_head_view', 'capital_expenditure_view')
        for view in table_view:
            dct['rows'][view] = {}
            for index, row in enumerate(params.get(view).get('rows')):
                if invalid(row, ['budget_head_id']):
                    continue
                values = {'budget_head_id': row.get('budget_head_id'),
                          'project_fy_id': project_fy_id}

                dct['rows'][view][index] = {}
                if row.get('goa_id') or row.get('goa_amount'):
                    values['amount'] = empty_to_none(row.get('goa_amount'))
                    submodel, created = model.objects.get_or_create(id=row.get('goa_id'), defaults=values)
                    if not created:
                        submodel = save_model(submodel, values)
                    if not row.get('goa_amount') and row.get('goa_id'):
                        model.objects.get(id=row.get('goa_id')).delete()
                    dct['rows'][view][index]['goa_id'] = submodel.id
                for aid in params.get('count'):
                    if row.get(aid) or row.get(aid + '-id'):
                        values['aid_id'] = aid.split('-')[0]
                        values['amount'] = empty_to_none(row.get(aid))
                        submodel, created = model.objects.get_or_create(id=row.get(aid + '-id'), defaults=values)
                        if not created:
                            submodel = save_model(submodel, values)
                        if not row.get(aid) and row.get(aid + '-id'):
                            model.objects.get(id=row.get(aid + '-id')).delete()
                        dct['rows'][view][index][aid + '-id'] = submodel.id
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    delete_budget_allocation(params.get('budget_head_view').get('deleted_rows'), model)
    delete_budget_allocation(params.get('capital_expenditure_view').get('deleted_rows'), model)
    return JsonResponse(dct)


def delete_budget_allocation(rows, model):
    for row in rows:
        for o in row.get('aid_amount'):
            if o.get('id'):
                try:
                    instance = model.objects.get(id=o.get('id'))
                    instance.delete()
                except:
                    pass
        if row.get('goa_id'):
            try:
                instance = model.objects.get(id=row.get('goa_id'))
                instance.delete()
            except:
                pass


class BudgetAllocation(ProjectFYView, BaseStatement, ListView):
    model = BudgetAllocationItem
    fy = None


@login_required
def save_budget_allocation(request):
    return base_save(request, BudgetAllocationItem)


class BudgetRelease(ProjectFYView, BaseStatement, ListView):
    model = BudgetReleaseItem
    fy = None


@login_required
def save_budget_release(request):
    return base_save(request, BudgetReleaseItem)


class BudgetExpenditure(ProjectFYView, BaseStatement, ListView):
    model = Expenditure
    fy = None
    template_name = 'project/expenditure_list.html'

    def get_queryset(self):
        if not self.model.objects.filter(project_fy_id=self.kwargs['project_fy_id']):
            return BudgetReleaseItem.objects.filter(project_fy_id=self.kwargs['project_fy_id'])
        return self.model.objects.filter(project_fy_id=self.kwargs['project_fy_id'])


@login_required
def save_expenditure(request):
    return base_save(request, Expenditure)


class ImprestJVView(ProjectFYView):
    model = ImprestJournalVoucher
    form_class = ImprestJVForm

    def get_context_data(self, **kwargs):
        context_data = super(ImprestJVView, self).get_context_data(**kwargs)
        if 'form' in context_data:
            instance = context_data['form'].instance
            context_data['data'] = {
                'jv': ImprestJVSerializer(instance).data,
                'dr_ledgers': AccountSerializer(self.project_fy.dr_ledgers(), many=True).data,
                'cr_ledgers': AccountSerializer(self.project_fy.cr_ledgers(), many=True).data,
            }
        return context_data

    def get_success_url(self):
        return reverse_lazy('imprest_journal_voucher_list', kwargs={'project_fy_id': self.project_fy.id})


class ImprestJVCreate(ImprestJVView, ProjectCreateView):
    pass


class ImprestJVUpdate(ImprestJVView, UpdateView):
    pass


class ImprestJVList(ImprestJVView, ListView):
    pass


class ImprestLedger(ImprestJVView, ListView):
    template_name = 'project/imprestledger_list.html'

    def get_queryset(self):
        qs = super(ImprestLedger, self).get_queryset()
        return qs.filter(Q(dr_id=self.kwargs.get('account_id')) | Q(cr_id=self.kwargs.get('account_id')))

    def get_context_data(self, **kwargs):
        context = super(ImprestLedger, self).get_context_data()
        account_id = self.kwargs.get('account_id')
        context['account'] = Account.objects.get(id=account_id)
        return context


class ImprestJVDelete(ImprestJVView, DeleteView):
    pass


class ReimbursementView(ProjectFYView):
    model = Reimbursement
    form_class = ReimbursementForm

    def get_success_url(self):
        return reverse_lazy('reimbursement_list', kwargs={'project_fy_id': self.project_fy.id})


class ReimbursementCreate(ReimbursementView, ProjectCreateView):
    pass


class ReimbursementUpdate(ReimbursementView, UpdateView):
    template_name = 'project/reimbursement_list.html'

    def get_context_data(self, **kwargs):
        context_data = super(ReimbursementUpdate, self).get_context_data(**kwargs)
        context_data['object_list'] = self.model.objects.filter(project_fy_id=context_data['project_fy'].id)
        return context_data


class ReimbursementList(ReimbursementView, ListView):
    pass


class ReimbursementDelete(ReimbursementView, DeleteView):
    pass


def statement_of_fund_template(request, project_fy_id):
    return render(request, 'project/statement_of_funds.html')


def memorandum_statement(request, project_fy_id):
    return render(request, 'project/memorandum_statement.html')


def ledgers(request, project_fy_id):
    project_fy = ProjectFy.objects.get(id=project_fy_id)
    context = {'accounts': project_fy.get_ledgers(), 'project_fy': project_fy}
    return render(request, 'project/ledger_list.html', context)


def aid_disbursement(request, project_fy_id):
    return render(request, 'project/aid_disbursement.html')


class DisbursementDetailView(ProjectFYView):
    model = DisbursementDetail
    form_class = DisbursementDetailForm

    def get_success_url(self):
        return reverse_lazy('disbursement_detail_list', kwargs={'project_fy_id': self.project_fy.id})

    def get_context_data(self, **kwargs):
        context = super(DisbursementDetailView, self).get_context_data(**kwargs)
        if 'form' in context:
            form = context['form']
            form.fields['aid'].widget.attrs.update(
                {'data-url': reverse_lazy('aid_add', kwargs={'project_id': context['project_fy'].project.id})})
        return context


class DisbursementDetailList(DisbursementDetailView, ListView):
    pass


class DisbursementDetailCreate(DisbursementDetailView, TemplateView):
    serializer_class = DisbursementDetailSerializer
    template_name = "project/disbursementdetail_form.html"

    def get_context_data(self, **kwargs):
        context = super(DisbursementDetailCreate, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = int(self.kwargs.get('pk'))
            obj = get_object_or_404(self.model, pk=pk, project_fy=context['project_fy'])
            scenario = 'Update'
        else:
            obj = self.model(project_fy=context['project_fy'])
            scenario = 'Create'
        data = self.serializer_class(obj).data
        aids = Aid.objects.filter(active=True, project=context['project_fy'].project)
        expense_category = ExpenseCategory.objects.all()
        context['data'] = data
        context['scenario'] = scenario
        context['obj'] = obj
        context['data']['aids'] = AidSerializer(aids, many=True).data
        context['data']['expense_category'] = ExpenseCategorySerializer(expense_category, many=True).data
        return context


class DisbursementDetailUpdate(DisbursementDetailView, UpdateView):
    pass


class DisbursementDetailDelete(DisbursementDetailView, DeleteView):
    pass


def save_disbursement_detail(request):
    params = json.loads(request.body)
    project_fy_id = params.get('project_fy')
    dct = {'rows': {}}
    object_values = {'wa_no': empty_to_none(params.get('wa_no')),
                     'requested_date': params.get('requested_date'), 'project_fy_id': project_fy_id,
                     'aid_id': params.get('aid_id'), 'remarks': params.get('remarks'),
                     'disbursement_method': params.get('disbursement_method'), }
    if params.get('id'):
        obj = DisbursementDetail.objects.get(id=params.get('id'))
    else:
        obj = DisbursementDetail()
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = DisbursementParticulars
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['expense_category_id']):
                continue
            # else:
            values = {'expense_category_id': row.get('expense_category_id'),
                      'request_nrs': row.get('request_nrs'), 'request_usd': row.get('request_usd'),
                      'request_sdr': row.get('request_sdr'),
                      'response_nrs': row.get('response_nrs'), 'response_usd': row.get('response_usd'),
                      'response_sdr': row.get('response_sdr'),
                      'with_held_nrs': row.get('with_held_nrs'), 'with_held_usd': row.get('with_held_usd'),
                      'with_held_sdr': row.get('with_held_sdr'),
                      'disbursement_detail': obj}

            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][ind] = submodel.id
        delete_rows(params.get('table_view').get('deleted_rows'), model)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    return JsonResponse(dct)

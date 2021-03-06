from django import http
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import user_passes_test

from app.utils.forms import form_view
from core.forms import EmployeeForm, DonorForm, BudgetHeadForm, CurrencyForm

from core.models import Employee, BudgetHead, Donor, Activity, TaxScheme, Language, FISCAL_YEARS, FiscalYear, Currency

from core.serializers import EmployeeSerializer, BudgetSerializer, ActivitySerializer, DonorSerializer, \
    TaxSchemeSerializer, LanguageSerializer
from django.views.generic import ListView
from users.models import group_required
from .signals import fiscal_year_signal
from app.utils.mixins import AjaxableResponseMixin, UpdateView, CreateView, DeleteView




@group_required('Store Keeper', 'Chief', 'Accountant')
def list_employees(request):
    objects = Employee.objects.all()
    return render(request, 'list_employees.html', {'objects': objects})


@group_required('Store Keeper', 'Chief', 'Accountant')
@form_view
def employee_form(request, id=None):
    return {
        'model': Employee,
        'form': EmployeeForm,
        'serializer': EmployeeSerializer,
        'listing_url': 'list_employees',
        'template': 'employee_form.html'
    }


@group_required('Store Keeper', 'Chief', 'Accountant')
def delete_employee(request, id):
    obj = get_object_or_404(Employee, id=id)
    obj.delete()
    return redirect(reverse('list_employees'))


@group_required('Store Keeper', 'Chief', 'Accountant')
def employees_as_json(request):
    objects = Employee.objects.all()
    objects_data = EmployeeSerializer(objects).data
    return JsonResponse(objects_data, safe=False)


def budget_heads_as_json(request):
    objects = BudgetHead.objects.all()
    objects_data = BudgetSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def donors_as_json(request):
    objects = Donor.objects.all()
    objects_data = DonorSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def activities_as_json(request):
    objects = Activity.objects.all()
    objects_data = ActivitySerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)

def tax_schemes_as_json(request):
    objects = TaxScheme.objects.all()
    objects_data = TaxSchemeSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def languages_as_json(request):
    objects = Language.objects.all()
    objects_data = LanguageSerializer(objects, many=True).data
    return JsonResponse(objects_data, safe=False)


def change_calendar(request):
    nxt = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=nxt, host=request.get_host()):
        nxt = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=nxt, host=request.get_host()):
            nxt = '/'
    response = http.HttpResponseRedirect(nxt)
    if request.method == 'POST':
        cal_code = request.POST.get('calendar')
        if cal_code and hasattr(request, 'session'):
            request.session['sess_cal'] = cal_code
    return response


@user_passes_test(lambda u: u.is_superuser)
def change_fiscal_year(request):
    if request.POST:
        old_fiscal_year = FiscalYear.get()
        new_fiscal_year_str = request.POST.get('fiscal_year')

        # app_setting.fiscal_year = new_fiscal_year_str
        # from dbsettings.models import Setting

        # fiscal_year_setting = Setting.objects.get(module_name='core.models', attribute_name='fiscal_year')
        # fiscal_year_setting.value = new_fiscal_year_str
        # fiscal_year_setting.save()
        from core.models import AppSetting
        app_setting = AppSetting.get_solo()
        app_setting.fiscal_year = new_fiscal_year_str
        app_setting.save()
        new_fiscal_year = FiscalYear.get(new_fiscal_year_str)
        fiscal_year_signal.send(sender=None, new_fiscal_year_str=new_fiscal_year_str, old_fiscal_year=old_fiscal_year,
                                new_fiscal_year=new_fiscal_year)

    context = {
        'has_permission': True, # required for user tools to show at admin
        'fiscal_years': FISCAL_YEARS,
        'current_fiscal_year': FiscalYear.get()
    }
    return render(request, 'change_fiscal_year.html', context)



class DonorView(object):
    model = Donor
    success_url = reverse_lazy('donor_list')
    form_class = DonorForm


class DonorList(DonorView, ListView):
    pass


class DonorCreate(AjaxableResponseMixin, DonorView, CreateView):
    pass


class DonorUpdate(DonorView, UpdateView):
    pass


class DonorDelete(DonorView, DeleteView):
    pass


class BudgetHeadView(object):
    model = BudgetHead
    success_url = reverse_lazy('budget_head_list')
    form_class = BudgetHeadForm


class BudgetHeadList(BudgetHeadView, ListView):
    pass


class BudgetHeadCreate(AjaxableResponseMixin, BudgetHeadView, CreateView):
    pass


class BudgetHeadUpdate(BudgetHeadView, UpdateView):
    pass


class BudgetHeadDelete(BudgetHeadView, DeleteView):
    pass



class CurrencyView(object):
    model = Currency
    success_url = reverse_lazy('currencies_list')
    form_class = CurrencyForm


class CurrencyList(CurrencyView, ListView):
    pass


class CurrencyCreate(AjaxableResponseMixin, CurrencyView, CreateView):
    pass


class CurrencyUpdate(CurrencyView, UpdateView):
    pass


class CurrencyDelete(CurrencyView, DeleteView):
    pass


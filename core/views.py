from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from account.serializers import AccountSerializer
from app.libr import form_view
from core.forms import PartyForm, EmployeeForm
from core.models import Party, Employee, Budget, Donor, Activity, Account, TaxScheme
from core.serializers import PartySerializer, EmployeeSerializer, BudgetSerializer, ActivitySerializer, DonorSerializer, TaxSchemeSerializer
from users.models import group_required
import json


@group_required('Store Keeper', 'Chief', 'Accountant')
def list_parties(request):
    objects = Party.objects.all()
    return render(request, 'list_parties.html', {'objects': objects})


@group_required('Store Keeper', 'Chief', 'Accountant')
def party_form(request, id=None):
    if id:
        obj = get_object_or_404(Party, id=id)
        scenario = 'Update'
    else:
        obj = Party()
        scenario = 'Create'
    if request.POST:
        form = PartyForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': PartySerializer(obj).data})
            return redirect(reverse('list_parties'))
    else:
        form = PartyForm(instance=obj)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'base.html'
    return render(request, 'party_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@group_required('Store Keeper', 'Chief', 'Accountant')
def delete_party(request, id):
    obj = get_object_or_404(Party, id=id)
    obj.delete()
    return redirect(reverse('list_parties'))


@group_required('Store Keeper', 'Chief', 'Accountant')
def parties_as_json(request):
    objects = Party.objects.all()
    objects_data = PartySerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


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
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


def budget_heads_as_json(request):
    objects = Budget.objects.all()
    objects_data = BudgetSerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


def donors_as_json(request):
    objects = Donor.objects.all()
    objects_data = DonorSerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


def activities_as_json(request):
    objects = Activity.objects.all()
    objects_data = ActivitySerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


def accounts_as_json(request):
    objects = Account.objects.all()
    objects_data = AccountSerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


def tax_schemes_as_json(request):
    objects = TaxScheme.objects.all()
    objects_data = TaxSchemeSerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")
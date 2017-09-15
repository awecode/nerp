from __future__ import division

import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils import timezone
from django.views.generic import UpdateView

from app import settings
from app.utils.mixins import CreateView, DeleteView, AjaxableResponseMixin
from app.utils.mixins import UpdateView as CustomUpdateView
from django.views.generic import ListView

from core.models import FiscalYear
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType

from .salary_gen_helpers import get_deduction, get_allowance, get_incentive, combine_deduction_details, \
    get_pro_tempore_data
from .serializers import PayrollEntrySerializer, ReportHRSerializer
from users.models import group_required, all_group_required
from .forms import GroupPayrollForm, EmployeeIncentiveFormSet, EmployeeForm, \
    IncentiveNameForm, IncentiveNameFormSet, AllowanceNameForm, AllowanceNameFormSet, \
    IncomeTaxSchemeForm, IncomeTaxCalcSchemeFormSet, IncomeTaxSchemeFormSet, MaritalStatusForm, \
    IncentiveNameDetailFormSet, GetReportForm, \
    EmployeeGradeFormSet, EmployeeGradeGroupFormSet, DesignationFormSet, ReportHrForm, ReportHrTableFormSet, \
    DeductionNameFormSet, GradeScaleValidityForm, AllowanceValidityForm, DeductionValidityForm, PayrollConfigForm, \
    PayrollAccountantForm, BranchOfficeForm, ProTemporeForm, EmployeeGradeNumberPauseFormset, TaxDeductionForm, \
    EmployeeFacilityFormSet, ReportTableForm, ReportTableDeatailForm
from .models import Employee, Deduction, EmployeeAccount, IncomeTaxScheme, ProTempore, IncentiveName, AllowanceName, \
    DeductionDetail, AllowanceDetail, IncentiveDetail, PaymentRecord, PayrollEntry, Account, Incentive, Allowance, \
    MaritalStatus, ReportHR, BranchOffice, EmployeeGrade, EmployeeGradeGroup, Designation, DeductionName, \
    AllowanceValidity, DeductionValidity, GradeScaleValidity, PayrollConfig, PayrollAccountant, ProTemporeDetail, \
    TaxDeduction, TaxDetail, EmployeeFacility, ReportTable, ReportTableDetail
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from calendar import monthrange as mr
from njango.nepdate import bs, ad2bs
from .models import get_y_m_tuple_list
from .bsdate import BSDate, get_bs_datetime, date_str_repr
from .helpers import are_side_months, bs_str2tuple, get_account_id, delta_month_date, delta_month_date_impure, \
    emp_salary_eligibility, month_cnt_inrange, fiscal_year_data, employee_last_payment_record, \
    emp_salary_eligibility_on_edit, get_validity_slots, get_validity_id, is_required_data_present, \
    user_is_branch_accountant, GroupRequiredMixin, IsBranchAccountantMixin, getattr_custom, json_file_to_dict, \
    get_property_methods, get_all_field_options, get_m2m_filter_options, get_y_m_in_words
from account.models import set_transactions, JournalEntry
from .filters import EmployeeFilter, PayrollEntryFilter
from django.core import serializers

from django.http.request import QueryDict

# Taxation singleton setting dbsettings
F_TAX_DISCOUNT_LIMIT = 300000
M_TAX_DISCOUNT_LIMIT = 200000
SOCIAL_SECURITY_TAX_RATE = 1


def verify_request_date(request):
    CALENDAR = PayrollConfig.get_solo().hr_calendar
    error = {}
    paid_from_date = None
    paid_to_date = None
    if request.POST:
        if CALENDAR == 'AD':
            try:
                # Validate it for bsdate
                paid_from_date = datetime.strptime(
                    request.POST.get('paid_from_date', None), '%Y-%m-%d').date()
            except:
                error['paid_from_date'] = 'Incorrect Date Format'
            try:
                paid_to_date = datetime.strptime(
                    request.POST.get('paid_to_date', None), '%Y-%m-%d').date()
            except:
                error['paid_to_date'] = 'Incorrect Date Format'

        else:
            try:

                paid_from_date = BSDate(*bs_str2tuple(
                    request.POST.get('paid_from_date', None)
                ))

            except:
                error['paid_from_date'] = 'Incorrect BS Date'
            try:
                paid_to_date = BSDate(*bs_str2tuple(
                    request.POST.get('paid_to_date', None)
                ))
            except:
                error['paid_to_date'] = 'Incorrect BS Date'

        if paid_from_date:
            error['global_errors'] = []
            try:
                get_validity_id(GradeScaleValidity, paid_from_date)
            except IOError:
                error['global_errors'].append(
                    'Given from date is to early for given Grade Scale Validities'
                )

            try:
                get_validity_id(AllowanceValidity, paid_from_date)
            except IOError:
                error['global_errors'].append(
                    'Given from date is to early for given Allowance Validities'
                )

            try:
                get_validity_id(DeductionValidity, paid_from_date)
            except IOError:
                error['global_errors'].append(
                    'Given from date is to early for given Deduction Validities'
                )

            if paid_to_date:
                if paid_to_date < paid_from_date:
                    error['global_errors'].append(
                        'Date: paid to must be greater than paid from'
                    )
            if not error['global_errors']:
                del error['global_errors']

        if error:
            return error
        else:
            # monthly_payroll = request.POST.get(
            #     'is_monthly_payroll',
            #     None
            # )
            # if monthly_payroll == u'true':
            #     if isinstance(paid_from_date, date):
            #         to_month_days = mr(
            #             paid_to_date.year,
            #             paid_to_date.month
            #         )[1]
            #         paid_from_date = date(
            #             paid_from_date.year,
            #             paid_from_date.month,
            #             1
            #         )
            #         paid_to_date = date(
            #             paid_to_date.year,
            #             paid_to_date.month,
            #             to_month_days
            #         )
            #
            #     else:
            #         to_month_days = bs[
            #             paid_to_date.year][
            #             paid_to_date.month - 1
            #             ]
            #         paid_from_date = BSDate(
            #             paid_from_date.year,
            #             paid_from_date.month,
            #             1
            #         )
            #         paid_to_date = BSDate(
            #             paid_to_date.year,
            #             paid_to_date.month,
            #             to_month_days
            #         )
            return paid_from_date, paid_to_date


def salary_taxation_unit(employee, f_y_item):
    # if CALENDAR == 'BS':
    #     CURRENT_FISCAL_YEAR = (
    #         BSDate(*FiscalYear.start()),
    #         BSDate(*FiscalYear.end())
    #     )


    # First calculate all the uncome of employee

    taxation_unit_errors = []

    required_present = False
    r_p_errors = []
    try:
        required_present, r_p_errors = is_required_data_present(employee, f_y_item['f_y'][0], f_y_item['f_y'][1])
    except IOError:
        taxation_unit_errors.append(
            'No Grade Scale Data data for fiscal year %s to %s' % (f_y_item['f_y'][0], f_y_item['f_y'][1]));

    if not required_present:
        taxation_unit_errors += r_p_errors

    salary = employee.get_date_range_salary(
        *f_y_item['f_y'],
        apply_grade_rate=True
    )
    # scale_salary = employee.get_date_range_salary(
    #     *f_y_item['f_y']
    # )

    allowance, a_errors = get_allowance(employee, from_date=f_y_item['f_y'][0],
                                        to_date=f_y_item['f_y'][1], request_from_tax_unit=True)

    taxation_unit_errors += a_errors

    incentive, i_errors = get_incentive(employee, from_date=f_y_item['f_y'][0],
                                        to_date=f_y_item['f_y'][1], request_from_tax_unit=True)

    taxation_unit_errors += i_errors

    facility_value = 0
    for facility in employee.facilities.all():
        facility_value += (facility.rate / 100) * salary

    salary += allowance + incentive + facility_value


    total_deduction, d_errors = get_deduction(
        employee,
        role='deduction',
        request_from_tax_unit=True,
        paid_from_date=f_y_item['f_y'][0],
        paid_to_date=f_y_item['f_y'][1]
    )

    # 1/3 of total deduction
    # FIXME previously it was 300000 i kept 30000 for now (later find the truth and fix)
    deductable_limit = (1 / 3.0) * salary if (1 / 3.0) * salary < 30000 else 30000
    deductatble_from_deduction = 0
    if total_deduction <= deductable_limit:
        deductatble_from_deduction = total_deduction
    else:
        deductatble_from_deduction = deductable_limit

    deduction_from_yearly_insurance_premium = employee.yearly_insurance_premium if employee.yearly_insurance_premium < 20000 else 20000

    taxation_unit_errors += d_errors

    taxable_amount = (salary - deductatble_from_deduction - deduction_from_yearly_insurance_premium)

    # import ipdb
    # ipdb.set_trace()

    if employee.marital_status == 'M':
        taxable_amount -= PayrollConfig.get_solo().married_remuneration_discount
        social_security_tax = PayrollConfig.get_solo().married_remuneration_discount / 100.0
    else:
        taxable_amount -= PayrollConfig.get_solo().unmarried_remuneration_discount
        social_security_tax = PayrollConfig.get_solo().unmarried_remuneration_discount / 100.0

    if employee.is_disabled_person:
        taxable_amount -= (PayrollConfig.get_solo().disabled_remuneration_additional_discount / 100.0) * taxable_amount



    subtracted_allowance = get_allowance(employee, from_date=f_y_item['f_y'][0],
                                         to_date=f_y_item['f_y'][1], role='tax_allowance')[0]
    subtracted_incentive = get_incentive(employee, from_date=f_y_item['f_y'][0],
                                         to_date=f_y_item['f_y'][1], role='tax_incentive')[0]
    taxable_amount -= subtracted_allowance + subtracted_incentive


    if taxable_amount < 0:
        taxable_amount = 0

    tax_amount = 0
    tax_schemes = sorted(
        IncomeTaxScheme.objects.filter(
            marital_status__marital_status=employee.marital_status
        ), key=lambda obj: obj.priority)
    main_loop_break_flag = False
    for obj in tax_schemes:
        # if obj.end_to:

        if (taxable_amount >= obj.start_from and
                    taxable_amount <= obj.end_to if obj.end_to else True):
            tax_calc_scheme = sorted(
                obj.tax_calc_scheme.all(),
                key=lambda x: x.priority
            )
            for obj2 in tax_calc_scheme:
                if obj.end_to != obj2.end_to:
                    tax_amount += obj2.end_to * obj2.tax_rate / 100
                    taxable_amount -= obj2.end_to
                else:
                    tax_amount += taxable_amount * obj2.tax_rate / 100
                    main_loop_break_flag = True
                    break
        if main_loop_break_flag:
            break

    if tax_amount < 0:
        tax_amount = 0

    if employee.sex == 'F' and tax_amount > 0:
        tax_amount -= (PayrollConfig.get_solo().female_remuneration_tax_discount / 100.0) * tax_amount
    remuneration_tax = tax_amount  # yearly
    social_security_tax  # yearly
    return social_security_tax * (f_y_item['worked_days'] / f_y_item['year_days']), remuneration_tax * (
        f_y_item['worked_days'] / f_y_item['year_days']), taxation_unit_errors


# @login_required
# @group_required('Accountant', 'Payroll Accountant')
# @user_passes_test(user_is_branch_accountant)
def get_employee_salary_detail(employee, paid_from_date, paid_to_date, eligibility_check_on_edit, edit_row):
    row_errors = []
    if not eligibility_check_on_edit:
        eligible, error = emp_salary_eligibility(
            employee,
            paid_from_date,
            paid_to_date,
        )

    else:
        # import ipdb
        # ipdb.set_trace()
        eligible, error = emp_salary_eligibility_on_edit(
            paid_from_date,
            paid_to_date,
            employee,
            edit_row
        )
    if not eligible:
        row_errors.append(error)

    required_present, r_p_errors = is_required_data_present(employee, paid_from_date, paid_to_date)

    if not required_present:
        row_errors += r_p_errors
        salary, scale_salary = 0, 0

    else:
        # This should be in if when we combine both monthly and daily payroll
        salary = employee.get_date_range_salary(
            paid_from_date,
            paid_to_date,
            apply_grade_rate=True
        )
        # scale_salary = employee.get_date_range_salary(
        #     paid_from_date,
        #     paid_to_date
        # )
    employee_response = {}
    employee_response['paid_employee'] = str(employee.id)
    employee_response['employee_grade'] = employee.designation.grade.grade_name
    employee_response['employee_designation'] = employee.designation.designation_name

    employee_response['allowance'], employee_response['allowance_details'], a_errors = get_allowance(
        employee,
        from_date=paid_from_date,
        to_date=paid_to_date
    )

    row_errors += a_errors

    # now calculate incentive if it has but not to add to salary just to
    # transact seperately

    employee_response['incentive'], employee_response['incentive_details'], i_errors = get_incentive(
        employee,
        from_date=paid_from_date,
        to_date=paid_to_date
    )
    row_errors += i_errors

    addition_from_deduction, addition_from_deduction_details = get_deduction(
        employee,
        role='addition',
        paid_from_date=paid_from_date,
        paid_to_date=paid_to_date
    )

    # salary += employee_response['incentive'] + employee_response['allowance'] + addition_from_deduction

    employee_response['deduced_amount'], deduction_details, d_errors = get_deduction(
        employee,
        role='deduction',
        paid_from_date=paid_from_date,
        paid_to_date=paid_to_date
    )
    row_errors += d_errors

    employee_response['deduction_details'] = combine_deduction_details(deduction_details,
                                                                       addition_from_deduction_details)

    # import ipdb
    # ipdb.set_trace()
    # PF deduction amount in case of loan from PF

    # Income tax logic
    f_y_data = fiscal_year_data(paid_from_date, paid_to_date)

    social_security_tax = 0
    remuneration_tax = 0
    if not row_errors:
        for item in f_y_data:
            s_tax, r_tax, taxation_errors = salary_taxation_unit(
                employee,
                item
            )

            if not taxation_errors:
                social_security_tax += s_tax
                remuneration_tax += r_tax
            else:
                row_errors += taxation_errors

    tax_details = []
    for tax_deduction in TaxDeduction.objects.all():

        if tax_deduction.code_name == "Social Security Tax":
            tax_details.append({
                'id': tax_deduction.id,
                'name': tax_deduction.name,
                'amount': round(social_security_tax,3)
            })
        elif tax_deduction.code_name == "Remuneration Tax":
            tax_details.append({
                'id': tax_deduction.id,
                'name': tax_deduction.name,
                'amount': round(remuneration_tax,3)
            })

    employee_response['tax_details'] = tax_details
    employee_response['pro_tempore_details'] = get_pro_tempore_data(employee)
    # First allowence added to salary for deduction and income tax.
    # For pure salary here added allowance should be duduced
    employee_response['salary'] = salary
    # employee_response['employee_bank_account_id'] = get_account_id(
    #     employee, 'bank_account')

    # employee_response['paid_amount'] = salary - deduction - income_tax + \
    #                                    p_t_amount + incentive + allowance

    if row_errors:
        for item in employee_response:
            if item not in ('paid_employee', 'employee_grade', 'employee_designation'):
                employee_response[item] = 0
        employee_response['row_errors'] = row_errors

        # if isinstance(paid_from_date, date):
        #     employee_response['paid_from_date'] = '{:%Y-%m-%d}'.format(paid_from_date)
        #     employee_response['paid_to_date'] = '{:%Y-%m-%d}'.format(paid_to_date)
        # else:
        # employee_response['paid_from_date'] = paid_from_date.as_string()
        # employee_response['paid_to_date'] = paid_to_date.as_string()
    employee_response['disable_input'] = True
    # employee_response['emp_options'] = []
    employee_response['emp_options'] = [{
        'id': employee.id,
        'name': employee.name,
    }]
    return employee_response


# Create your views here.
@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def payroll_entry(request, pk=None):
    accountant_branch_id = request.user.payroll_accountant.branch.id
    if pk:
        entry = PayrollEntry.objects.get(pk=pk)
        form_initial = {'payroll_type': 'GROUP', 'branch': entry.branch}
        serializer = PayrollEntrySerializer(entry)
        ctx_data = dict(serializer.data)
    else:
        form_initial = {'payroll_type': 'GROUP'}
        ctx_data = {'computed_scenario': 'CREATE',}
    main_form = GroupPayrollForm(initial=form_initial, accountant_branch_id=accountant_branch_id)

    # Inititial employee options
    employees = Employee.objects.all()
    emp_opt_list = [{'name': e.name, 'id': str(e.id)} for e in employees]

    ko_data = {
        'ctx_data': ctx_data,
        'emp_options': emp_opt_list,
        'calendar': PayrollConfig.get_solo().hr_calendar
    }

    return render(
        request,
        'payroll_entry.html',
        {
            'm_form': main_form,
            'ko_data': ko_data
        })


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def get_employee_account(request):
    response = {}
    error = {}
    if request.POST:
        employee_id = request.POST.get('paid_employee', None)
        if employee_id:
            employee = Employee.objects.get(id=int(employee_id))
        else:
            error['employee'] = 'No such employee'

        edit = request.POST.get('edit')
        dates = verify_request_date(request)

        if isinstance(dates, tuple):
            paid_from_date, paid_to_date = dates
        else:
            error.update(dates)

        if error:
            response['errors'] = error
            return JsonResponse(response)

        # Now calculate all the values and give a good meaningful response
        # total_work_day = paid_to_date - paid_from_date

        # Check for eligibility check
        eligibility_check_on_edit = False
        edit_row = None
        if edit:
            p_e = PayrollEntry.objects.get(id=edit)
            emp_entry_rows = p_e.entry_rows.all().filter(paid_employee=employee)
            if not emp_entry_rows:
                eligibility_check_on_edit = False
            else:
                eligibility_check_on_edit = True
                edit_row = emp_entry_rows[0]

        response['data'] = get_employee_salary_detail(
            employee,
            paid_from_date,
            paid_to_date,
            eligibility_check_on_edit,
            edit_row
        )

        # response.update(resp)
        return JsonResponse(response)
    else:
        return HttpResponse('Damn no request.POST')


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def get_employees_account(request):
    error = {}
    response = {}
    data_list = []
    if request.POST:
        dates = verify_request_date(request)
        if isinstance(dates, tuple):
            paid_from_date, paid_to_date = dates
        else:
            error.update(dates)

        if error:
            response['errors'] = error
            return JsonResponse(response)

        branch = request.POST.get('branch', None)
        edit = request.POST.get('edit')
        employee_type = request.POST.get('employee_type')

        employees = Employee.objects.filter(status='ACTIVE')
        if branch != 'ALL':
            employees = employees.filter(working_branch__id=int(branch))

        if employee_type != 'ALL':
            employees = employees.filter(type=employee_type)

        for employee in employees:
            # data_dict = {'employee_id': employee.id}
            eligibility_check_on_edit = False
            edit_row = None
            if edit:
                p_e = PayrollEntry.objects.get(id=edit)
                emp_entry_rows = p_e.entry_rows.all().filter(paid_employee=employee)
                if not emp_entry_rows:
                    eligibility_check_on_edit = False
                else:
                    eligibility_check_on_edit = True
                    edit_row = emp_entry_rows[0]
            employee_salary_detail = get_employee_salary_detail(
                employee,
                paid_from_date,
                paid_to_date,
                eligibility_check_on_edit,
                edit_row
            )

            # data_dict.update(employee_salary_detail)
            data_list.append(employee_salary_detail)

        response['data'] = data_list
        return JsonResponse(response)


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def save_payroll_entry(request, pk=None):
    CALENDAR = PayrollConfig.get_solo().hr_calendar
    if request.POST:
        params = json.loads(request.body)
        save_response = {}

        is_monthly_payroll = True if params.get('is_monthly_payroll', None) else False
        # if branch is ALL then save it as None
        request_branch = params.get('branch', None)
        branch = None if request_branch == 'ALL' else int(request_branch)

        payment_records = []
        # paid_from_date_for_p_e = params.get('paid_from_date')
        # paid_to_date_for_p_e = params.get('paid_to_date')
        if (CALENDAR == 'AD'):
            paid_from_date_for_p_e = datetime.strptime(params.get('paid_from_date'), '%Y-%m-%d')
            paid_to_date_for_p_e = datetime.strptime(params.get('paid_from_date'), '%Y-%m-%d')
        else:
            paid_from_date_for_p_e = params.get('paid_from_date')
            paid_to_date_for_p_e = params.get('paid_to_date')
        # p_e_date_range_set = False
        # import ipdb
        # ipdb.set_trace()
        with transaction.atomic():
            if pk:
                p_e = PayrollEntry.objects.get(id=pk)
            else:
                p_e = PayrollEntry.objects.create(
                    branch_id=branch,
                    is_monthly_payroll=is_monthly_payroll,
                    paid_from_date=paid_from_date_for_p_e,
                    paid_to_date=paid_to_date_for_p_e
                )
            for row in params.get('entry_rows'):

                if row.get('id'):
                    p_r = PaymentRecord.objects.get(id=row.get('id'))
                    p_r.deduction_details.all().delete()
                    p_r.incentive_details.all().delete()
                    p_r.allowance_details.all().delete()
                    p_r.pro_tempore_details.all().delete()
                    p_r.tax_details.all().delete()
                else:
                    p_r = PaymentRecord()

                # p_r = PaymentRecord()
                p_r.paid_employee_id = int(row.get('paid_employee', None))

                p_r.designation = Employee.objects.get(id=p_r.paid_employee_id).designation
                # Save according to calender settin`g
                # from_date = request.POST.get('form-%d-paid_from_date' % (i), None)
                # to_date = request.POST.get('form-%d-paid_to_date' % (i), None)

                p_r.paid_from_date = paid_from_date_for_p_e
                p_r.paid_to_date = paid_to_date_for_p_e

                p_r.absent_days = row.get('absent_days', 0)
                p_r.deduced_amount = float(row.get('deduced_amount', None))

                p_r.allowance = float(row.get('allowance', None))
                p_r.incentive = float(row.get('incentive', None))
                # p_r.pro_tempore_amount = float(row.get('pro_tempore_amount', None))
                p_r.salary = float(row.get('salary', None))
                p_r.paid_amount = float(row.get('paid_amount', None))
                p_r.entry = p_e
                p_r.save()

                # Similar if we need all details of incentive and allowence
                for ded in row.get('deduction_details', []):
                    amount = float(ded['amount'])
                    amount_added_before_deduction = float(ded['amount_added_before_deduction'])
                    if amount:
                        DeductionDetail.objects.create(
                            deduction_id=ded['deduction'],
                            amount=amount,
                            amount_added_before_deduction=amount_added_before_deduction,
                            payment_record=p_r
                        )
                for allowance_name in row.get('allowance_details', []):
                    amount = float(allowance_name['amount'])
                    if amount:
                        AllowanceDetail.objects.create(
                            allowance_id=allowance_name['allowance'],
                            amount=amount,
                            payment_record=p_r
                        )

                for incentive_name in row.get('incentive_details', []):
                    amount = float(incentive_name['amount'])
                    if amount:
                        IncentiveDetail.objects.create(
                            incentive_id=incentive_name['incentive'],
                            amount=amount,
                            payment_record=p_r
                        )

                paid_pro_tempore_ids = []
                for pro_tempore in row.get('pro_tempore_details', []):
                    amount = float(pro_tempore['amount'])
                    paid_pro_tempore_ids.append(pro_tempore['p_t_id'])
                    ProTemporeDetail.objects.create(
                        pro_tempore_id=pro_tempore['p_t_id'],
                        amount=amount,
                        payment_record=p_r
                    )

                for tax in row.get('tax_details', []):
                    amount = float(tax['amount'])
                    if amount:
                        TaxDetail.objects.create(
                            tax_deduction_id=tax['id'],
                            amount=amount,
                            payment_record=p_r
                        )

                # Set pro tempore status to paid
                for pt in ProTempore.objects.filter(id__in=paid_pro_tempore_ids):
                    pt.status = 'PAID'
                    pt.save()
                    # End Set pro tempore status to paid

                    # payment_records.append(p_r.id)
            # p_e = PayrollEntry()

            # PayrollEntry.objects.create(
            #     entry_row=payment_records,
            # )
            save_response['entry_id'] = p_e.id
            save_response['entry_saved'] = True
            save_response['entry_approved'] = False
            save_response['entry_transacted'] = False
            return JsonResponse(save_response)  # Should have permissions


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def approve_entry(request, pk=None):
    payroll_entry = PayrollEntry.objects.get(pk=pk)
    payroll_entry.approved = True
    payroll_entry.save()
    if request.is_ajax():
        return JsonResponse({'entry_approved': True})
    else:
        return redirect(reverse('entry_list'))


# Should have permissions
@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def delete_entry(request, pk=None):
    payroll_entry = PayrollEntry.objects.get(pk=pk)
    payment_records_rows = payroll_entry.entry_rows.all()
    payment_recordid_set = [p.id for p in payment_records_rows]
    # pdb.set_trace()
    # payroll_entry.entry_row_set.clear()

    # Delete Transaction Here
    # delete_rows(
    #     payment_records_rows,
    #     PaymentRecord
    # )
    for pr_id in payment_recordid_set:
        p_r = PaymentRecord.objects.get(id=pr_id)
        record_deduction_details = [rdd.id for rdd in p_r.deduction_details.all()]
        record_allowance_details = [rad.id for rad in p_r.allowance_details.all()]
        record_incentive_details = [rid.id for rid in p_r.incentive_details.all()]
        record_pro_tempore_details = [rid.id for rid in p_r.pro_tempore_details.all()]
        record_tax_details = [rid.id for rid in p_r.tax_details.all()]

        paid_pro_tempore_ids = [rid.pro_tempore.id for rid in p_r.pro_tempore_details.all()]

        try:
            JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(PaymentRecord),
                                     object_id=p_r.id).delete()
        except:
            pass

        p_r.delete()

        DeductionDetail.objects.filter(id__in=record_deduction_details).delete()
        AllowanceDetail.objects.filter(id__in=record_allowance_details).delete()
        IncentiveDetail.objects.filter(id__in=record_incentive_details).delete()
        ProTemporeDetail.objects.filter(id__in=record_pro_tempore_details).delete()
        TaxDetail.objects.filter(id__in=record_tax_details).delete()

        # Change paid pro tempore status back to ready for payment
        for pt in ProTempore.objects.filter(id__in=paid_pro_tempore_ids):
            pt.status = 'READY_FOR_PAYMENT'
            pt.save()
            # End Change paid pro tempore status back to ready for payment

    payroll_entry.delete()

    return redirect(reverse('entry_list'))


# depreciated
@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def entry_detail(request, pk=None):
    # ko_data contains entry main properties
    ko_data = {}

    rows = []

    all_allowances = AllowanceName.objects.all()
    all_incentives = IncentiveName.objects.all()
    all_deductions = DeductionName.objects.all()

    allowance_titles = []
    incentive_titles = []
    deduction_titles = []

    for ob in all_allowances:
        a_title = _(ob.name.title())
        allowance_titles.append(a_title)
    for ob in all_incentives:
        i_title = _(ob.name.title())
        incentive_titles.append(i_title)
    for ob in all_deductions:
        # if ob.deduction_for == 'EMPLOYEE ACC':
        #     d_name = '_'.join(ob.in_acc_type.name.split(' ')).lower()
        # else:
        d_name = '_'.join(ob.name.split(' ')).lower()
        d_title = ' '.join(d_name.split('_')).title()
        deduction_titles.append(d_title)

    if pk:
        p_e = PayrollEntry.objects.get(id=pk)
        ko_data['entry_id'] = p_e.id
        ko_data['entry_approved'] = p_e.approved
        ko_data['entry_transacted'] = p_e.transacted

        entry_rows = p_e.entry_rows.all()

        paid_from_date = entry_rows[0].paid_from_date
        paid_to_date = entry_rows[0].paid_to_date
        branch = p_e.branch.name if p_e.branch else "From All Branch"

        if isinstance(paid_from_date, date):
            paid_from_date = '{:%Y/%m/%d}'.format(entry_rows[0].paid_from_date)
            paid_to_date = '{:%Y/%m/%d}'.format(entry_rows[0].paid_from_date)

        for row in entry_rows:
            entry_row_data = {}
            emp = row.paid_employee
            entry_row_data['employee'] = (emp)
            entry_row_data['employee_designation'] = (row.designation)
            entry_row_data['employee_grade'] = (row.designation.grade)

            allowance_amounts = []
            for obj in all_allowances:
                a_amount = 0
                for allowance_n, amount in [(a.allowance, a.amount) for a in row.allowance_details.all()]:
                    if obj == allowance_n:
                        a_amount = amount
                        break
                allowance_amounts.append(a_amount)
            entry_row_data['allowance_data'] = allowance_amounts
            entry_row_data['total_allowance'] = (row.allowance)

            incentive_amounts = []
            for obj in all_incentives:
                i_amount = 0
                for incentive_n, amount in [(a.incentive, a.amount) for a in row.incentive_details.all()]:
                    if obj == incentive_n:
                        i_amount = amount
                        break
                incentive_amounts.append(i_amount)
            entry_row_data['incentive_data'] = incentive_amounts
            entry_row_data['total_incentive'] = (row.incentive)

            deduction_amounts = []
            for obj in all_deductions:
                d_amount = 0
                for deduction, amount in [(a.deduction, a.amount) for a in row.deduction_details.all()]:
                    if obj == deduction:
                        d_amount = amount
                        break
                deduction_amounts.append(d_amount)
            entry_row_data['deduction_data'] = deduction_amounts
            entry_row_data['deduced_amount'] = row.deduced_amount

            entry_row_data['income_tax'] = (row.income_tax)
            entry_row_data['pro_tempore_amount'] = (row.pro_tempore_amount)
            entry_row_data['salary'] = (row.salary)
            entry_row_data['paid_amount'] = (row.paid_amount)
            rows.append(entry_row_data)

        return render(
            request,
            'entry_detail.html',
            {
                'paid_from_date': paid_from_date,
                'paid_to_date': paid_to_date,
                'branch': branch,
                'rows': rows,
                'allowance_titles': allowance_titles,
                'incentive_titles': incentive_titles,
                'deduction_titles': deduction_titles,
                'ko_data': ko_data
            }
        )


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def entry_list(request):
    accountant_branch_id = request.user.payroll_accountant.branch.id
    data = request.GET.copy()
    data.setdefault('branch', accountant_branch_id)
    objects = PayrollEntryFilter(data, queryset=PayrollEntry.objects.all(),
                                 accountant_branch_id=accountant_branch_id)
    # entries = PayrollEntry.objects.all()
    return render(
        request,
        'entry_list.html',
        {
            'objects': objects,
        }
    )
    pass


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def get_employee_options(request):
    if request.POST:
        # pdb.set_trace()
        branch = request.POST.get('branch', None)
        employee_type = request.POST.get('employee_type', None)
        employees = Employee.objects.filter(status='ACTIVE')
        if branch and employee_type:
            if branch != 'ALL':
                employees = employees.filter(working_branch__id=int(branch))
            if employee_type != 'ALL':
                employees = employees.filter(type=employee_type)
            opt_list = [{'name': e.name, 'id': str(e.id)} for e in employees]
            return JsonResponse({'opt_data': opt_list})
        else:
            return HttpResponse('No branch')
    else:
        return HttpResponse('No POST')


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def transact_entry(request, pk=None):
    p_e = PayrollEntry.objects.get(id=pk)

    salary_giving_account = Account.objects.get(
        category=PayrollConfig.get_solo().salary_giving_account_category,
        name='Salary Giving Account',
        fy=FiscalYear.get()
    )

    with transaction.atomic():
        for entry in p_e.entry_rows.all():
            employee = entry.paid_employee
            salary = entry.salary

            salary_giving_cr_amount = 0
            # salary_giving_dr_amount = 0

            emp_basic_salary_cr_amount = 0
            emp_basic_salary_dr_amount = 0

            # Here
            salary_giving_cr_amount += salary
            emp_basic_salary_dr_amount += salary

            # Transact Pro Tempore
            protempore_account = Account.objects.get(
                category=PayrollConfig.get_solo().pro_tempore_account_category,
                employee_account__employee=employee,
                fy=FiscalYear.get()
            )
            pro_tempore_amount = entry.pro_tempore_amount

            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    # ('cr', salary_giving_account, pro_tempore_amount),
                    ('dr', protempore_account, pro_tempore_amount),
                ]
            )
            # Here
            salary_giving_cr_amount += pro_tempore_amount

            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    ('cr', protempore_account, pro_tempore_amount),
                    # ('dr', emp_basic_salary_account, pro_tempore_amount),
                ]
            )

            # Here
            emp_basic_salary_dr_amount += pro_tempore_amount

            for allowance_details_item in entry.allowance_details.all():
                a_account = Account.objects.get(
                    category=allowance_details_item.allowance.account_category,
                    employee_account__employee=employee,
                    fy=FiscalYear.get()
                )
                a_amount = allowance_details_item.amount

                # Should be changed
                set_transactions(
                    entry,
                    p_e.entry_datetime,
                    *[
                        # ('cr', salary_giving_account, a_amount),
                        ('dr', a_account, a_amount),
                    ]
                )

                # Here
                salary_giving_cr_amount += a_amount

                set_transactions(
                    entry,
                    p_e.entry_datetime,
                    *[
                        # ('dr', employee_salary_account, a_amount),
                        ('cr', a_account, a_amount),
                        # ('dr', emp_basic_salary_account, a_amount),
                    ]
                )

                # Here
                emp_basic_salary_dr_amount += a_amount

            for incentive_details_item in entry.incentive_details.all():
                i_account = Account.objects.get(
                    category=incentive_details_item.incentive.account_category,
                    employee_account__employee=employee,
                    fy=FiscalYear.get()
                )
                i_amount = incentive_details_item.amount

                set_transactions(
                    entry,
                    p_e.entry_datetime,
                    *[
                        # ('cr', salary_giving_account, i_amount),
                        ('dr', i_account, i_amount),
                    ]
                )

                # Here
                salary_giving_cr_amount += i_amount

                set_transactions(
                    entry,
                    p_e.entry_datetime,
                    *[
                        ('cr', i_account, i_amount),
                        # ('dr', emp_basic_salary_account, i_amount),
                    ]
                )

                # Here
                emp_basic_salary_dr_amount += i_amount

            for tax in entry.tax_details.all():
                t_account = Account.objects.get(
                    category=tax.tax_deduction.account_category,
                    employee_account__employee=employee,
                    fy=FiscalYear.get()
                )
                t_amount = tax.amount

                set_transactions(
                    entry,
                    p_e.entry_datetime,
                    *[
                        # ('cr', emp_basic_salary_account, t_amount),
                        ('dr', t_account, t_amount),
                    ]
                )

                # Here
                emp_basic_salary_cr_amount += t_amount

                # set_transactions(
                #     entry,
                #     p_e.entry_datetime,
                #     *[
                #         ('cr', t_account, t_amount),
                #         ('dr', salary_giving_account, t_amount),
                #     ]
                # )

            for deduction_details_item in entry.deduction_details.all():
                deduction_obj = deduction_details_item.deduction
                d_account = a_account = Account.objects.get(
                    category=deduction_obj.deduct_in_category,
                    employee_account__employee=employee,
                    fy=FiscalYear.get()
                )

                d_amount = deduction_details_item.amount

                set_transactions(
                    entry,
                    p_e.entry_datetime,
                    *[
                        # ('cr', emp_basic_salary_account, d_amount),
                        ('dr', d_account, d_amount),
                    ]
                )

                # Here
                emp_basic_salary_cr_amount += d_amount

                if employee.type == 'PERMANENT' and deduction_details_item.deduction.first_add_to_salary:
                    add_before_deduction_account = Account.objects.get(
                        category=deduction_obj.deduct_in_category.children.all()[0],
                        employee_account__employee=employee,
                        fy=FiscalYear.get()
                    )
                    amount_added_before_deduction = deduction_details_item.amount_added_before_deduction

                    set_transactions(
                        entry,
                        p_e.entry_datetime,
                        *[
                            # ('cr', salary_giving_account, amount_added_before_deduction),
                            ('dr', add_before_deduction_account, amount_added_before_deduction),
                        ]
                    )

                    # Here
                    salary_giving_cr_amount += amount_added_before_deduction

                    set_transactions(
                        entry,
                        p_e.entry_datetime,
                        *[
                            ('cr', add_before_deduction_account, amount_added_before_deduction),
                            # ('dr', emp_basic_salary_account, amount_added_before_deduction),
                        ]
                    )

                    # Here
                    emp_basic_salary_dr_amount += amount_added_before_deduction

            # NeedUpdate
            emp_basic_salary_account = Account.objects.get(
                category=PayrollConfig.get_solo().basic_salary_account_category,
                employee_account__employee=employee,
                fy=FiscalYear.get()
            )
            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    ('cr', salary_giving_account, salary_giving_cr_amount),

                    # ('cr', emp_basic_salary_account, emp_basic_salary_cr_amount),
                    ('dr', emp_basic_salary_account, emp_basic_salary_dr_amount - emp_basic_salary_cr_amount),
                ]
            )

    p_e.transacted = True
    p_e.save()
    if request.is_ajax():
        return JsonResponse({'entry_transacted': True})
    else:
        return redirect(reverse('entry_list'))


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def employee(request, pk=None):
    accountant_branch_id = request.user.payroll_accountant.branch.id
    ko_data = {}

    if pk:
        obj_id = pk
        employee = Employee.objects.get(id=pk)
    else:
        obj_id = None
        employee = Employee()

    if request.method == "POST":
        employee_form = EmployeeForm(request.POST, instance=employee, accountant_branch_id=accountant_branch_id,
                                     prefix='emp_form')
        employee_incentive_formset = EmployeeIncentiveFormSet(request.POST, instance=employee, prefix='emp_inc_formset')
        employee_grade_number_pause_formset = EmployeeGradeNumberPauseFormset(request.POST, instance=employee,
                                                                              prefix='emp_gnp_formset')

        if employee_form.is_valid() and employee_incentive_formset.is_valid() and employee_grade_number_pause_formset.is_valid():
            employee_form.save()
            employee_incentive_formset.save()
            employee_grade_number_pause_formset.save()
            return redirect(reverse('list_employee'))
    else:
        employee_form = EmployeeForm(instance=employee, accountant_branch_id=accountant_branch_id, prefix='emp_form')
        employee_incentive_formset = EmployeeIncentiveFormSet(instance=employee, prefix='emp_inc_formset')
        employee_grade_number_pause_formset = EmployeeGradeNumberPauseFormset(instance=employee,
                                                                              prefix='emp_gnp_formset')

    return render(
        request,
        'employee_cu.html',
        {
            'employee_form': employee_form,
            'employee_incentive_formset': employee_incentive_formset,
            'employee_grade_number_pause_formset': employee_grade_number_pause_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def list_employee(request):
    accountant_branch_id = request.user.payroll_accountant.branch.id
    data = request.GET.copy()
    data.setdefault('working_branch', accountant_branch_id)
    data.setdefault('type', 'PERMANENT')
    data.setdefault('status', 'ACTIVE')
    objects = EmployeeFilter(data, queryset=Employee.objects.all(),
                             accountant_branch_id=accountant_branch_id)
    return render(
        request,
        'employee_list.html',
        {
            'objects': objects,
        }
    )


@login_required
@group_required('Accountant')
def allowance(request, pk=None):
    CALENDAR = PayrollConfig.get_solo().hr_calendar
    allowance_validity_form = AllowanceValidityForm()
    allowance_name_form = AllowanceNameForm()
    return render(
        request,
        'allowance.html',
        {
            'calendar': CALENDAR,
            'av_form': allowance_validity_form,
            'allowance_name_form': allowance_name_form
        }
    )


@login_required
@group_required('Accountant')
def deduction_name(request):
    if request.method == "POST":

        deduction_formset = DeductionNameFormSet(
            request.POST,
            queryset=DeductionName.objects.all(),
        )
        if deduction_formset.is_valid():
            deduction_formset.save()
            return redirect(reverse('deduction_name'))
    else:
        deduction_formset = DeductionNameFormSet(
            queryset=DeductionName.objects.all(),
        )
    return render(
        request,
        'deduction_cu.html',
        {
            'deduction_formset': deduction_formset,
        })


@login_required
@group_required('Accountant')
def deduction(request):
    deduction_validity_form = DeductionValidityForm()
    return render(
        request,
        'deduction.html',
        {
            'dv_form': deduction_validity_form
        }
    )


@login_required
@group_required('Accountant')
def employee_grade(request):
    if request.method == "POST":

        employee_grade_formset = EmployeeGradeFormSet(
            request.POST,
            queryset=EmployeeGrade.objects.all(),
        )
        if employee_grade_formset.is_valid():
            employee_grade_formset.save()
            return redirect(reverse('employee_grade'))
    else:
        employee_grade_formset = EmployeeGradeFormSet(
            queryset=EmployeeGrade.objects.all(),
        )

    return render(
        request,
        'employee_grade_cu.html',
        {
            'employee_grade_formset': employee_grade_formset,
        })


@login_required
@group_required('Accountant')
def employee_grade_group(request):
    if request.method == "POST":

        employee_grade_group_formset = EmployeeGradeGroupFormSet(
            request.POST,
            queryset=EmployeeGradeGroup.objects.all(),
        )
        if employee_grade_group_formset.is_valid():
            employee_grade_group_formset.save()
            return redirect(reverse('employee_grade_group'))
    else:
        employee_grade_group_formset = EmployeeGradeGroupFormSet(
            queryset=EmployeeGradeGroup.objects.all(),
        )

    return render(
        request,
        'employee_grade_group_cu.html',
        {
            'employee_grade_group_formset': employee_grade_group_formset,
        })


@login_required
@group_required('Accountant')
def employee_designation(request):
    if request.method == "POST":

        designation_formset = DesignationFormSet(
            request.POST,
            queryset=Designation.objects.all(),
        )
        if designation_formset.is_valid():
            designation_formset.save()
            return redirect(reverse('employee_designation'))
    else:
        designation_formset = DesignationFormSet(
            queryset=Designation.objects.all(),
        )

    return render(
        request,
        'employee_designation_cu.html',
        {
            'designation_formset': designation_formset,
        })


@login_required
@group_required('Accountant')
def tax_scheme_detail(request, pk=None):
    ko_data = {}

    if pk:
        obj_id = pk
        tax_scheme = IncomeTaxScheme.objects.get(id=pk)
    else:
        obj_id = None
        tax_scheme = IncomeTaxScheme()

    if request.method == "POST":
        tax_scheme_form = IncomeTaxSchemeForm(request.POST, instance=tax_scheme)
        tax_calc_scheme_formset = IncomeTaxCalcSchemeFormSet(request.POST, instance=tax_scheme)
        if tax_scheme_form.is_valid() and tax_calc_scheme_formset.is_valid():
            tax_scheme_form.save()
            tax_calc_scheme_formset.save()
            return redirect(reverse('list_tax_scheme'))
    else:
        tax_scheme_form = IncomeTaxSchemeForm(instance=tax_scheme)
        tax_calc_scheme_formset = IncomeTaxCalcSchemeFormSet(instance=tax_scheme)

    return render(
        request,
        'tax_detail_scheme_cu.html',
        {
            'tax_scheme_form': tax_scheme_form,
            'tax_calc_scheme_formset': tax_calc_scheme_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


@login_required
@group_required('Accountant')
def list_tax_scheme(request):
    m_objects = sorted(
        IncomeTaxScheme.objects.filter(marital_status__marital_status='M'),
        key=lambda x: x.priority
    )
    u_objects = sorted(
        IncomeTaxScheme.objects.filter(marital_status__marital_status='U'),
        key=lambda x: x.priority
    )
    return render(
        request,
        'tax_scheme_list.html',
        {
            'm_objects': m_objects,
            'u_objects': u_objects,
        }
    )


@login_required
@group_required('Accountant')
def tax_scheme(request, pk=None):
    ko_data = {}

    if pk:
        obj_id = pk
        marital_status = MaritalStatus.objects.get(id=pk)
    else:
        obj_id = None
        marital_status = MaritalStatus()

    if request.method == "POST":
        marital_status_form = MaritalStatusForm(request.POST, instance=marital_status)
        tax_scheme_formset = IncomeTaxSchemeFormSet(request.POST, instance=marital_status)
        if marital_status_form.is_valid() and tax_scheme_formset.is_valid():
            marital_status_form.save()
            tax_scheme_formset.save()
            return redirect(reverse('list_tax_scheme'))
    else:
        marital_status_form = MaritalStatusForm(instance=marital_status)
        tax_scheme_formset = IncomeTaxSchemeFormSet(instance=marital_status)

    return render(
        request,
        'tax_scheme_cu.html',
        {
            'marital_status_form': marital_status_form,
            'tax_scheme_formset': tax_scheme_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


@login_required
@group_required('Accountant')
def delete_taxscheme(request, pk=None):
    obj = MaritalStatus.objects.get(id=pk)
    # alw_details = Allowance.objects.filter(name=obj)
    obj.delete()
    # for alw in alw_details():
    #     alw.delete()
    return redirect(reverse('list_tax_scheme'))


@login_required
@group_required('Accountant')
def incentivename_curd(request):
    if request.method == "POST":

        incentivename_formset = IncentiveNameDetailFormSet(
            request.POST,
            queryset=IncentiveName.objects.all(),
        )
        if incentivename_formset.is_valid():
            incentivename_formset.save()
            return redirect(reverse('incentivename_curd'))
    else:
        incentivename_formset = IncentiveNameDetailFormSet(
            queryset=IncentiveName.objects.all(),
        )

    return render(
        request,
        'incentivename_curd.html',
        {
            'incentivename_formset': incentivename_formset,
        })


@login_required
@group_required('Accountant')
def facility_curd(request):
    if request.method == "POST":

        employee_facility_formset = EmployeeFacilityFormSet(
            request.POST,
            queryset=EmployeeFacility.objects.all(),
        )
        if employee_facility_formset.is_valid():
            employee_facility_formset.save()
            return redirect(reverse('facility_curd'))
    else:
        employee_facility_formset = EmployeeFacilityFormSet(
            queryset=EmployeeFacility.objects.all(),
        )

    return render(
        request,
        'employeefacility_curd.html',
        {
            'employee_facility_formset': employee_facility_formset,
        })


@login_required
@group_required('Accountant', 'Payroll Accountant')
@user_passes_test(user_is_branch_accountant)
def get_report(request):
    accountant_branch_id = request.user.payroll_accountant.branch.id
    if request.method == "POST":
        report_request_query = GetReportForm(request.POST, accountant_branch_id=accountant_branch_id)
        if report_request_query.is_valid():
            report = report_request_query.cleaned_data.get('report')
            branch = report_request_query.cleaned_data.get('branch')

            employee_type = report_request_query.cleaned_data.get('employee_type')
            
            employee_bank = report_request_query.cleaned_data.get('employee_bank')

            employee_bank_branch = report_request_query.cleaned_data.get('employee_bank_branch')

            employee_with_deduction = report_request_query.cleaned_data.get('employee_with_deduction')

            employee = report_request_query.cleaned_data.get('employee')

            from_date = report_request_query.cleaned_data.get('from_date')
            to_date = report_request_query.cleaned_data.get('to_date')
            distinguish_entry = report_request_query.cleaned_data.get('distinguish_entry')

            branch_qry = {'paid_employee__working_branch': branch}

            if employee:
                branch_qry['paid_employee'] = employee

            if employee_bank:
                branch_qry['paid_employee__bank'] = employee_bank

            if employee_bank_branch:
                branch_qry['paid_employee__bank_branch'] = employee_bank_branch

            if employee_type != 'ALL':
                branch_qry['paid_employee__type'] = employee_type

            if employee_with_deduction:
                branch_qry['paid_employee__optional_deductions'] = employee_with_deduction

            months = get_y_m_in_words(from_date, to_date)
            # import ipdb
            # ipdb.set_trace()
            context = {
                'organization_title': PayrollConfig.get_solo().organization_title.split(','),
                'report_title': report.name,
                'branch': branch,
                'from_date': from_date,
                'to_date': to_date,
                'months': months,
                'distinguish_entry': distinguish_entry,
                'employee': employee,
                'employee_bank': employee_bank,
                'employee_bank_branch': employee_bank_branch,
            }

            if distinguish_entry:
                payment_record_list = [(
                                           p_e.entry_rows.filter(**branch_qry), get_bs_datetime(
                                               p_e.entry_datetime,
                                               p_e.entry_date,
                                               format=PayrollConfig.get_solo().hr_calendar
                                           ), (
                                               date_str_repr(p_e.paid_from_date,
                                                             format=PayrollConfig.get_solo().hr_calendar),
                                               date_str_repr(p_e.paid_to_date,
                                                             format=PayrollConfig.get_solo().hr_calendar),
                                           ), get_y_m_in_words(from_date, to_date)

                                       ) for p_e in PayrollEntry.objects.filter(
                    paid_from_date__gte=from_date,
                    paid_to_date__lte=to_date,
                )]

            else:
                payment_records = PaymentRecord.objects.filter(
                    paid_from_date__gte=from_date,
                    paid_to_date__lte=to_date,
                    **branch_qry)
                payment_record_list = [(payment_records, None)]

            template_path = '/'.join(report.template.split('/')[-2:])

            record_table_list = []

            tables = []
            for payment_record in payment_record_list:

                # create table data here
                report_tables = report.report_tables.all()
                record_table = {}
                for table in report_tables:
                    fields = table.table_details.order_by('order')

                    # TODO in future: make table using multiple rowspan and colspan of heading by assigning field parent text
                    # TODO above is my first approach also think of other approach

                    # Table field data is composed of (actual data, rowspan, colsapan)
                    record_table['name'] = table.title
                    record_table['data'] = [[(field.field_name, 1, 1) for field in fields]]
                    # TODO check fields order by ipdb

                    total_fields = [[_('Total'), 1, 1]]
                    for i, fld in enumerate(fields):
                        if fld.need_total:
                            total_fields.append([0, 1, 1])
                        else:
                            total_fields.append(['', 1, 1])

                    for record in payment_record[0]:
                        field_data = []
                        for i, field in enumerate(fields):
                            value = getattr_custom(
                                record, field.field_description
                            )
                            field_data.append(
                                (value, 1, 1)
                            )
                            if field.need_total:
                                total_fields[i + 1][0] += value
                        record_table['data'].append(field_data)
                    record_table['data'].append(total_fields)

                    # This works only if we have one table( multiple table may lead to confustion)
                    context['totals_row'] = total_fields

                    # TODO manage rowspan and colspan of total fields here and push it to record_table[data]
                    if distinguish_entry:
                        record_table['entry_datetime'] = payment_record[
                            1]  # Tuple date, time
                        record_table['date_range'] = payment_record[
                            2]  # Tuple from, to
                        record_table['included_months'] = payment_record[
                            3]  # Tuple from, to
                    tables.append(record_table)

            context['tables'] = tables
            context['today'] = timezone.now().date() if PayrollConfig.get_solo().hr_calendar == 'AD' else BSDate(*ad2bs(timezone.now().date()))
            # TODO include totals array into context (works only when we have one table report)
            # context['tables'] = tables

            return render(request, template_path, context)

        else:
            return render(request, 'get_report.html', {'get_report_form': report_request_query})
    else:
        get_report_form = GetReportForm(accountant_branch_id=accountant_branch_id)
        return render(request, 'get_report.html', {'get_report_form': get_report_form})


@login_required
@group_required('Accountant')
def report_setting(request, pk=None):
    ko_data = {}

    if pk:
        ko_data['obj_id'] = pk
        hr_report = ReportHR.objects.get(id=pk)
        serializer = ReportHRSerializer(hr_report)
        ko_data['ctx_data'] = dict(serializer.data)
    else:
        ko_data['obj_id'] = None
        ko_data['ctx_data'] = None
        # hr_report = ReportHR()

    if request.method == "POST":
        if pk:
            report_hr = ReportHR.objects.get(id=pk)
        else:
            report_hr = ReportHR()
        params = json.loads(request.body)

        try:
            with transaction.atomic():
                report_hr.name = params.get('name')
                report_hr.code = params.get('code')
                report_hr.template = params.get('template')
                # report_hr.for_employee_type = params.get('for_employee_type')
                report_hr.save()

                for table_to_dlt in params.get('to_remove'):
                    if table_to_dlt.get('id'):
                        ReportTable.objects.get(id=table_to_dlt.get('id')).delete()

                for report_table_data in params.get('report_tables'):
                    if report_table_data.get('id'):
                        report_table = ReportTable.objects.get(id=report_table_data.get('id'))
                    else:
                        report_table = ReportTable()
                    report_table.title = report_table_data.get('title')
                    report_table.report = report_hr
                    report_table.save()

                    for field_to_dlt in report_table_data.get('to_remove'):
                        if field_to_dlt.get('id'):
                            ReportTableDetail.objects.get(id=field_to_dlt.get('id')).delete()

                    for table_details_data in report_table_data.get('table_details'):
                        if table_details_data.get('id'):
                            table_detail = ReportTableDetail.objects.get(id=table_details_data.get('id'))
                        else:
                            table_detail = ReportTableDetail()

                        table_detail.field_name = table_details_data.get('field_name')
                        table_detail.field_description = table_details_data.get('field_description')
                        table_detail.order = table_details_data.get('order')
                        table_detail.need_total = table_details_data.get('need_total', False)
                        table_detail.table = report_table
                        table_detail.save()

            return JsonResponse({"success": True})

        except Exception, e:
            return JsonResponse({"success": False, "message": str(e)})

    else:
        hr_report_form = ReportHrForm()
        report_table_form = ReportTableForm()
        report_table_detail_form = ReportTableDeatailForm()

        return render(
            request,
            'hr_report_cu.html',
            {
                'hr_report_form': hr_report_form,
                'report_table_form': report_table_form,
                'report_table_detail_form': report_table_detail_form,
                'ko_data': ko_data,
            })


@login_required
@group_required('Accountant')
def load_selected_options(request):
    # deduction_details___deduction__code_name = pf - deduction;__amount
    res = {}
    selected_options = []

    report_model = PaymentRecord
    params = json.loads(request.body)
    query = params.get('query')
    model = report_model
    for qi, qry in enumerate(query.split(';')):
        splitted_12m_qry = qry.split('___')
        for i, qr in enumerate(splitted_12m_qry[0].split('__')):
            if qr:
                if qr in get_property_methods(model):
                    selected_options.append(
                        {
                            'options': get_all_field_options(model),
                            'selected': ('%s') % qr
                        }
                    )
                else:
                    field_obj = model._meta.get_field(qr)
                    if field_obj.many_to_one or field_obj.one_to_one or field_obj.one_to_many or field_obj.many_to_many:

                        if len(splitted_12m_qry) == 2 and i == len(splitted_12m_qry[0].split('__')) - 1:
                            selected_options.append(
                                {
                                    'options': get_all_field_options(model),
                                    'selected': ('%s___') % qr
                                }
                            )
                        else:
                            selected_options.append(
                                {
                                    'options': get_all_field_options(model),
                                    'selected': ('%s__') % qr
                                }
                            )
                        model = field_obj.related_model
                    else:
                        selected_options.append(
                            {
                                'options': get_all_field_options(model),
                                'selected': ('%s') % qr
                            }
                        )
        if len(splitted_12m_qry) == 2:
            if splitted_12m_qry[1]:
                # filter generating options here
                selected_options.append(
                    {
                        'options': get_m2m_filter_options(model),
                        'selected': ('%s;__') % (splitted_12m_qry[1])
                    }
                )
    res['selected_options'] = selected_options
    return JsonResponse(res)


@login_required
@group_required('Accountant')
def get_report_field_options(request):
    # deduction_details___deduction__code_name = pf - deduction;__amount
    res = {}
    report_model = PaymentRecord
    params = json.loads(request.body)
    query = params.get('query')
    if not query:
        res['options'] = get_all_field_options(report_model)
        return JsonResponse(res)
    else:
        model = report_model
        for qi, qry in enumerate(query.split(';')):
            splitted_12m_qry = qry.split('___')
            for i, qr in enumerate(splitted_12m_qry[0].split('__')):
                if qr:
                    field_obj = model._meta.get_field(qr)
                    if field_obj.many_to_one or field_obj.one_to_one or field_obj.one_to_many or field_obj.many_to_many:
                        model = field_obj.related_model
                if not qr and i == len(splitted_12m_qry[0].split('__')) - 1:
                    res['options'] = get_all_field_options(model)
                    return JsonResponse(res)

            if len(splitted_12m_qry) == 2:
                if not splitted_12m_qry[1]:
                    # filter generating options here
                    res['options'] = get_m2m_filter_options(model)
                    return JsonResponse(res)

    return JsonResponse(res)


@login_required
@group_required('Accountant')
def list_report_setting(request):
    objects = ReportHR.objects.all()
    return render(
        request,
        'hr_report_list.html',
        {
            'objects': objects,
        }
    )


@login_required
@group_required('Accountant')
def delete_report_setting(request, pk=None):
    obj = ReportHR.objects.get(id=pk)
    # alw_details = Allowance.objects.filter(name=obj)
    obj.delete()
    # for alw in alw_details():
    #     alw.delete()
    return redirect(reverse('list_report_setting'))


@login_required
@group_required('Accountant')
def grades_scale(request):
    grade_scale_validity_form = GradeScaleValidityForm()
    return render(request, 'grades_scale.html', {
        'gsv_form': grade_scale_validity_form
    })


@login_required
@group_required('Accountant', 'Payroll Accountant')
def payroll_index(request):
    return render(request, 'hr_index.html', {})


class PayrollConfigUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = ('Accountant')
    model = PayrollConfig
    form_class = PayrollConfigForm
    # fields = ['name']
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return PayrollConfig.get_solo()

    def get_success_url(self):
        return reverse('payroll_entry')


class PayrollAccountantView(object):
    model = PayrollAccountant
    success_url = reverse_lazy('payroll_accountant_list')
    form_class = PayrollAccountantForm
    group_requied = ('Accountant')


class PayrollAccountantList(LoginRequiredMixin, GroupRequiredMixin, PayrollAccountantView, ListView):
    pass


class PayrollAccountantCreate(LoginRequiredMixin, GroupRequiredMixin, AjaxableResponseMixin, PayrollAccountantView,
                              CreateView):
    pass


class PayrollAccountantUpdate(LoginRequiredMixin, GroupRequiredMixin, PayrollAccountantView, CustomUpdateView):
    pass


class PayrollAccountantDelete(LoginRequiredMixin, GroupRequiredMixin, PayrollAccountantView, DeleteView):
    pass


class BranchView(object):
    model = BranchOffice
    success_url = reverse_lazy('branch_list')
    form_class = BranchOfficeForm
    group_requied = ('Accountant')


class BranchList(LoginRequiredMixin, GroupRequiredMixin, BranchView, ListView):
    pass


class BranchCreate(LoginRequiredMixin, GroupRequiredMixin, AjaxableResponseMixin, BranchView, CreateView):
    pass


class BranchUpdate(LoginRequiredMixin, GroupRequiredMixin, BranchView, CustomUpdateView):
    pass


class BranchDelete(LoginRequiredMixin, GroupRequiredMixin, BranchView, DeleteView):
    pass


# TODO show only of employee under
class ProTemporeView(object):
    model = ProTempore
    success_url = reverse_lazy('protempore_list')
    form_class = ProTemporeForm
    group_requied = ('Accountant, Payroll Accountant')


class ProTemporeList(LoginRequiredMixin, GroupRequiredMixin, IsBranchAccountantMixin, ProTemporeView, ListView):
    pass


class ProTemporeCreate(LoginRequiredMixin, GroupRequiredMixin, IsBranchAccountantMixin, AjaxableResponseMixin,
                       ProTemporeView, CreateView):
    pass


class ProTemporeUpdate(LoginRequiredMixin, GroupRequiredMixin, IsBranchAccountantMixin, ProTemporeView,
                       CustomUpdateView):
    pass


class ProTemporeDelete(LoginRequiredMixin, GroupRequiredMixin, IsBranchAccountantMixin, ProTemporeView, DeleteView):
    pass


class TaxDeductionView(object):
    model = TaxDeduction
    success_url = reverse_lazy('taxdeduction_list')
    form_class = TaxDeductionForm
    group_requied = ('Accountant')


class TaxDeductionList(LoginRequiredMixin, GroupRequiredMixin, TaxDeductionView, ListView):
    pass


class TaxDeductionCreate(LoginRequiredMixin, GroupRequiredMixin,
                         TaxDeductionView, CreateView):
    pass


class TaxDeductionUpdate(LoginRequiredMixin, GroupRequiredMixin, TaxDeductionView,
                         CustomUpdateView):
    pass


class TaxDeductionDelete(LoginRequiredMixin, GroupRequiredMixin, TaxDeductionView, DeleteView):
    pass

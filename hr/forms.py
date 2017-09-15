from django import forms
# from datetime import date
from django.forms import ModelChoiceField
from mptt.forms import TreeNodeChoiceField
from njango.nepdate import bs2ad

from hr.bsdate import BSDate
from hr.fields import HRBSFormField, HRBSDateFormField
from hr.helpers import bs_str2tuple, employee_last_payment_record, inc_1_day, drc_1_day
from users.models import User
from .models import PaymentRecord, PayrollEntry, BranchOffice, Employee, ReportHR, ReportTableDetail, EmployeeGrade, EmployeeGradeGroup, \
    Designation, ReportTable, DeductionName, GradeScaleValidity, AllowanceValidity, DeductionValidity, PayrollConfig, \
    PayrollAccountant, ProTempore, EmployeeGradeNumberPause, TaxDeduction, EmployeeFacility, Bank, BankBranch
from django.forms.widgets import Select, DateInput, NumberInput, CheckboxInput, DateTimeInput, TextInput   # , MultiWidget
from njango.fields import BSDateField, today
from django.utils.translation import ugettext_lazy as _
from .models import Deduction, IncentiveName, AllowanceName, Incentive, Allowance, EmployeeAccount, IncomeTaxScheme, \
    IncomeTaxCalcScheme, MaritalStatus
from account.models import Account
from app.utils.forms import HTML5BootstrapModelForm
import datetime


# Start Validity Forms
class GradeScaleValidityForm(HTML5BootstrapModelForm):
    class Meta:
        model = GradeScaleValidity
        fields = '__all__'

        widgets = {
            'valid_from': HRBSFormField(attrs={'data-bind': "value: valid_from"}),
            'note': TextInput(attrs={'data-bind': "value: note",})
        }


class AllowanceValidityForm(HTML5BootstrapModelForm):
    class Meta:
        model = AllowanceValidity
        fields = '__all__'
        widgets = {
            'valid_from': HRBSFormField(attrs={'data-bind': "value: valid_from"}),
            'note': TextInput(attrs={'data-bind': "value: note", })
        }


class DeductionValidityForm(HTML5BootstrapModelForm):
    class Meta:
        model = DeductionValidity
        fields = '__all__'

        widgets = {
            'valid_from': HRBSFormField(attrs={'data-bind': "value: valid_from"}),
            'note': TextInput(attrs={'data-bind': "value: note",})
        }


# End Validity Forms

class PayrollEntryForm(HTML5BootstrapModelForm):
    class Meta:
        model = PayrollEntry
        fields = '__all__'

        widgets = {
            'entry_row': NumberInput(attrs={}),
            'entry_datetime': DateTimeInput(attrs={})
        }


class GroupPayrollForm(forms.Form):

    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(GroupPayrollForm, self).__init__(*args, **kwargs)
        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.fields['branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.fields['branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)

    payroll_type = forms.ChoiceField(
        choices=[
            ('INDIVIDUAL', _('Individual')),
            ('GROUP', _('Group'))],
        widget=Select(attrs={'data-bind': 'value: payroll_type, disable: disable_main_input, selectize:{}'})
    )
    branch = TreeNodeChoiceField(
        queryset=BranchOffice.objects.all(),
        empty_label=None,
        widget=Select(attrs={'data-bind': 'value: branch, disable: disable_main_input, selectize:{}'})
    )
    employee_type_choices = (
        ('ALL', _('All Type')),
        ('PERMANENT', _('Permanent')),
        ('TEMPORARY', _('Temporary')),
    )
    employee_type = forms.ChoiceField(
        choices=employee_type_choices,
        widget=Select(attrs={'data-bind': 'value: employee_type, disable: disable_main_input, selectize:{}'})
    )

    from_date = HRBSDateFormField(
        widget=HRBSFormField(attrs={
            'data-bind': 'value: paid_from_date_input, disable: disable_main_input',
            'class': 'td-input-calendar',
            'placeholder': 'YYYY-MM-DD',
            'is_required': True
        }),
    )
    to_date = HRBSDateFormField(
        widget=HRBSFormField(attrs={
            'data-bind': 'value: paid_to_date_input, disable: disable_main_input',
            'class': 'td-input-calendar',
            'placeholder': 'YYYY-MM-DD',
            'is_required': True
        }),
    )


class GetReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(GetReportForm, self).__init__(*args, **kwargs)
        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.fields['branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.fields['branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)

    report = forms.ModelChoiceField(
        queryset=ReportHR.objects.all(),
        label=_('Select Report')
    )
    from_date = HRBSDateFormField(
        widget=HRBSFormField(attrs={
            'placeholder': 'YYYY-MM-DD',
        }),
        label=_('From Date')
    )
    to_date = HRBSDateFormField(
        widget=HRBSFormField(attrs={
            'placeholder': 'YYYY-MM-DD',
        }),
        label=_('To Date')
    )
    branch = TreeNodeChoiceField(
        widget=Select(attrs={"data-bind": "value:branch" }),
        queryset=BranchOffice.objects.all(),
        empty_label=None,
        label=_('Select Branch')
    )

    distinguish_entry = forms.BooleanField(
        label=_("Distinguish Entry"),
        required=False
    )
    emp_type_choices = (
        ('PERMANENT', _('Permanent')),
        ('TEMPORARY', _('Temporary')),
        ('ALL', _('All Type')),
    )
    employee_type = forms.ChoiceField(
        widget=Select(attrs={"data-bind": "value: employee_type"}),
        choices=emp_type_choices,
        label=_('Employee Type'),
        initial='ALL'
    )

    employee_bank = forms.ModelChoiceField(
        queryset=Bank.objects.all(),
        label=_('Employee Bank'),
        initial=None,
        required=False
    )

    employee_bank_branch = forms.ModelChoiceField(
        queryset=BankBranch.objects.all(),
        label=_('Employee Bank Branch'),
        initial=None,
        required=False
    )

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=Select(attrs={"data-bind": "options: employee_options, optionsText: 'name', optionsValue:'id', optionsCaption: 'Choose..'"}),
        label=_('Employee'), initial=None,
        required=False
    )

    employee_with_deduction = forms.ModelChoiceField(
        queryset=DeductionName.objects.all(),
        initial=None, label=_('Employee with deduction'),
        required=False
    )

    # distinguish

    def clean(self):
        cleaned_data = super(GetReportForm, self).clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date:
            if to_date < from_date:
                self.add_error(
                    'from_date',
                    _('From date must be less than to date')
                )


class EmployeeAccountInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            account_categories = []
            if form.cleaned_data:
                employee_acc = form.cleaned_data['account']
                account_category = employee_acc.category
                if account_category in account_categories:
                    raise forms.ValidationError(
                        _('Account should be unique.'))
                account_categories.append(
                    account_category
                )


class IncentiveInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                payment_cycle = form.cleaned_data.get("payment_cycle")
                year_payment_cycle_month = form.cleaned_data.get(
                    "year_payment_cycle_month")

                if payment_cycle == 'Y' and not year_payment_cycle_month:
                    form.add_error(
                        'year_payment_cycle_month',
                        _('This field is needed if it is a yearly allowance')
                    )


class EmployeeGradeNumberPauseInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        time_stamp_ranges = []
        for form in self.forms:
            form_is_clean = True
            if form.cleaned_data:
                from_date = form.cleaned_data.get("from_date")
                to_date = form.cleaned_data.get("to_date")
                employee = form.cleaned_data.get("employee")

                if from_date > to_date:
                    form_is_clean = False
                    form.add_error(
                        'from_date',
                        _('From date must be less than to date')
                    )

                last_paid = employee_last_payment_record(employee)
                if not last_paid:
                    last_paid = drc_1_day(employee.scale_start_date)

                if from_date < last_paid:
                    form_is_clean = False
                    form.add_error(
                        'from_date',
                        _('From date cannot be less than employee last paid date. Last paid on %(hrbs_date)s') % {'hrbs_date': str(last_paid)}
                    )

                for gnp in time_stamp_ranges:
                    if from_date <= gnp[1]:
                        form.add_error(
                            'from_date',
                            _('This range overlaps with previous range entry.'),
                        )
                        break
                if form_is_clean:
                    time_stamp_ranges.append((from_date, to_date))


class AllowanceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            if form.cleaned_data:
                sum_type = form.cleaned_data.get("sum_type")
                amount = form.cleaned_data.get("amount")
                amount_rate = form.cleaned_data.get("amount_rate")
                payment_cycle = form.cleaned_data.get("payment_cycle")
                year_payment_cycle_month = form.cleaned_data.get("year_payment_cycle_month")

                if sum_type == 'AMOUNT' and not amount:
                    form.add_error(
                        'amount',
                        'Need amount field to be filled up when Sum Type is Amount'
                    )
                elif sum_type == 'RATE' and not amount_rate:
                    form.add_error(
                        'amount_rate',
                        'Need amount rate field to be filled up when Sum Type is Rate'
                    )
                if payment_cycle == 'Y' and not year_payment_cycle_month:
                    form.add_error(
                        'year_payment_cycle_month',
                        'This field is needed if it is a yearly allowance'
                    )


class IncomeTaxSchemeInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(IncomeTaxSchemeInlineFormSet, self).clean()
        e_p_dict_list = []
        for form in self.forms:
            if form.cleaned_data:
                start_from = form.cleaned_data.get("start_from")
                end_to = form.cleaned_data.get("end_to")
                priority = form.cleaned_data.get("priority")
                DELETE = form.cleaned_data.get("DELETE")

                if end_to:
                    if end_to < start_from:
                        form.add_error(
                            'start_from',
                            'start_from must be less than end_to',
                        )

                if not DELETE:
                    e_p_dict_list.append({
                        'start_from': start_from,
                        'end_to': end_to,
                        'priority': priority,
                        'form': form})
        # sorted_dict_list = sorted(
        #     e_p_dict_list,
        #     key=lambda item: item['priority'],
        #     reverse=True
        # )
        sorted_dict_list = sorted(
            e_p_dict_list,
            key=lambda item: item['priority'],
            reverse=True
        )
        if sorted_dict_list:
            if sorted_dict_list[-1]['start_from'] != 0:
                sorted_dict_list[-1]['form'].add_error(
                    'start_from',
                    'First range must start from 0',
                )
            for index, item in enumerate(sorted_dict_list):
                if index == 0 and len(sorted_dict_list) > 1:

                    if item['end_to'] is not None:
                        item['form'].add_error(
                            'end_to',
                            'Last range end to should be None'
                        )
                    try:
                        if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
                            item['form'].add_error(
                                'start_from',
                                'start_from must be just after previous end_to',
                            )
                    except:
                        pass

                else:
                    if item['end_to'] is None:
                        item['form'].add_error(
                            'end_to',
                            'This field should not be None'
                        )
                    try:
                        if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
                            item['form'].add_error(
                                'start_from',
                                'start_from must be just after previous end_to',
                            )
                    except:
                        pass


class IncomeTaxCalcSchemeInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(IncomeTaxCalcSchemeInlineFormSet, self).clean()
        e_p_dict_list = []
        for form in self.forms:
            instance = self.instance
            if form.cleaned_data:
                start_from = form.cleaned_data.get("start_from")
                end_to = form.cleaned_data.get("end_to")
                priority = form.cleaned_data.get("priority")
                DELETE = form.cleaned_data.get("DELETE")

                if end_to:
                    if end_to < start_from:
                        form.add_error(
                            'start_from',
                            'start_from must be less than end_to',
                        )

                if not DELETE:
                    e_p_dict_list.append({
                        'start_from': start_from,
                        'end_to': end_to,
                        'priority': priority,
                        'form': form})
        sorted_dict_list = sorted(
            e_p_dict_list,
            key=lambda item: item['priority'],
            reverse=True
        )
        if sorted_dict_list:
            if sorted_dict_list[-1]['start_from'] != 0:
                sorted_dict_list[-1]['form'].add_error(
                    'start_from',
                    'First range must start from 0'
                )
            for index, item in enumerate(sorted_dict_list):
                if index == 0:
                    if not instance.end_to:
                        if item['end_to'] is not None:
                            item['form'].add_error(
                                'end_to',
                                'Last range end to should be None'
                            )
                    else:
                        if item['end_to'] != instance.end_to:
                            item['form'].add_error(
                                'end_to',
                                'Last range end to should be equal to %d' % instance.end_to,
                            )
                    try:
                        if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
                            item['form'].add_error(
                                'start_from',
                                'start_from must be just after previous end_to',
                            )
                    except:
                        pass

                else:
                    if item['end_to'] is None:
                        item['form'].add_error(
                            'end_to',
                            'This field should not be None'
                        )
                    try:
                        if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
                            item['form'].add_error(
                                'start_from',
                                'start_from must be just after previous end_to',
                            )
                    except:
                        pass


class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AllowanceForm, self).__init__(*args, **kwargs)
        choices = [(obj.id, obj.__unicode__()) for obj in
                   sorted(EmployeeGrade.objects.all(), key=lambda m: m.__unicode__())]
        self.fields['employee_grade'].widget = Select(choices=choices)

    def clean(self):
        cleaned_data = super(AllowanceForm, self).clean()
        payment_cycle = cleaned_data.get("payment_cycle")
        year_payment_cycle_month = cleaned_data.get("year_payment_cycle_month")

        if payment_cycle == 'Y' and not year_payment_cycle_month:
            self.add_error(
                'year_payment_cycle_month',
                'This field is needed if it is a yearly allowance'
            )


class IncentiveForm(forms.ModelForm):
    class Meta:
        model = Incentive
        fields = '__all__'

    def clean(self):
        cleaned_data = super(IncentiveForm, self).clean()

        payment_cycle = cleaned_data.get("payment_cycle")
        year_payment_cycle_month = cleaned_data.get("year_payment_cycle_month")

        if payment_cycle == 'Y' and not year_payment_cycle_month:
            self.add_error(
                'year_payment_cycle_month',
                'This field is needed if it is a yearly allowance'
            )


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = '__all__'



    # def clean(self):
    #     cleaned_data = super(DeductionForm, self).clean()
    #
    #     deduction_for = cleaned_data.get("deduction_for")
    #     explicit_acc = cleaned_data.get("explicit_acc")
    #     in_acc_type = cleaned_data.get("in_acc_type")
    #
    #     if deduction_for == 'EXPLICIT ACC' and not explicit_acc:
    #         self.add_error(
    #             'explicit_acc',
    #             'This field is required with Deduction for Explicit Account'
    #         )
    #     elif deduction_for == 'EMPLOYEE ACC' and not in_acc_type:
    #         self.add_error(
    #             'in_acc_type',
    #             'This field is required with Deduction for Employee Account'
    #         )

class EmployeeForm(HTML5BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['optional_deductions'].queryset = DeductionName.objects.filter(is_optional=True)
        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.fields['working_branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.fields['working_branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)

    working_branch = TreeNodeChoiceField(queryset=BranchOffice.objects.all())

    class Meta:
        model = Employee
        exclude = ('accounts', 'incentives', 'name_en', 'name_ne')


class IncentiveNameForm(HTML5BootstrapModelForm):
    class Meta:
        model = IncentiveName
        fields = '__all__'


class AllowanceNameForm(HTML5BootstrapModelForm):
    class Meta:
        model = AllowanceName
        fields = ('name', 'code_name', 'description', 'is_tax_free')
        widgets = {
            'name': TextInput(attrs={'data-bind': "value: name",}),
            'code_name': TextInput(attrs={'data-bind': "value: code_name",}),
            'description': TextInput(attrs={'data-bind': "value: description",}),
            'is_tax_free': CheckboxInput(attrs={'data-bind': "checked: is_tax_free",}),
        }


class MaritalStatusForm(HTML5BootstrapModelForm):
    class Meta:
        model = MaritalStatus
        fields = '__all__'


class IncomeTaxSchemeForm(HTML5BootstrapModelForm):
    class Meta:
        model = IncomeTaxScheme
        fields = '__all__'

        widgets = {
            'marital_status': Select(attrs={'readonly': "true"}),
            'start_from': NumberInput(attrs={'readonly': "true"}),
            'end_to': NumberInput(attrs={'readonly': "true"}),
            'priority': NumberInput(attrs={'readonly': "true"}),
        }


class ReportHrForm(HTML5BootstrapModelForm):
    class Meta:
        model = ReportHR
        # fields = '__all__'
        exclude = ('name_en', 'name_ne')

        widgets = {
         'name': TextInput(attrs={'data-bind': "value: name"}),
         'code': TextInput(attrs={'data-bind': "value: code"}),
         'template': Select(attrs={'data-bind': "value: template"}),
         # 'for_employee_type': Select(attrs={'data-bind': "value: for_employee_type"}),

        }


class ReportTableForm(HTML5BootstrapModelForm):
    class Meta:
        model = ReportTable
        exclude = ('title_en', 'title_ne', 'report')

        widgets = {
            'title': TextInput(attrs={'data-bind': "value: title"}),
        }


class ReportTableDeatailForm(HTML5BootstrapModelForm):
    class Meta:
        model = ReportTableDetail
        exclude = ('field_name_en', 'field_name_ne', 'table')

        widgets = {
            'field_name': TextInput(attrs={'data-bind': "value: field_name"}),
            'field_description': TextInput(attrs={'data-bind': "value: field_description"}),
            'order': NumberInput(attrs={'data-bind': "value: order"}),
            'need_total': CheckboxInput(attrs={'data-bind': "checked: need_total"}),

        }



# These are crud formset
EmployeeIncentiveFormSet = forms.inlineformset_factory(
    Employee,
    Incentive,
    extra=1,
    fields='__all__',
    formset=IncentiveInlineFormset
)

EmployeeGradeNumberPauseFormset = forms.inlineformset_factory(
    Employee,
    EmployeeGradeNumberPause,
    extra=1,
    fields='__all__',
    formset=EmployeeGradeNumberPauseInlineFormset
)

IncentiveNameFormSet = forms.inlineformset_factory(
    IncentiveName,
    Incentive,
    extra=1,
    exclude=('account',),
    formset=IncentiveInlineFormset
)
AllowanceNameFormSet = forms.inlineformset_factory(
    AllowanceName,
    Allowance,
    form=AllowanceForm,
    extra=1,
    exclude=('account',),
    formset=AllowanceInlineFormset
)

DeductionNameFormSet = forms.modelformset_factory(
    DeductionName,
    extra=1,
    can_delete=True,
    exclude=('deduct_in_category',),
)

EmployeeGradeFormSet = forms.modelformset_factory(
    EmployeeGrade,
    extra=1,
    can_delete=True,
    fields='__all__',
)

EmployeeGradeGroupFormSet = forms.modelformset_factory(
    EmployeeGradeGroup,
    extra=1,
    can_delete=True,
    fields='__all__',
)


class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)
        choices = [(obj.id, obj.__unicode__())  for obj in sorted(EmployeeGrade.objects.all(),  key=lambda m: m.__unicode__())]
        self.fields['grade'].widget = Select(choices=choices)

DesignationFormSet = forms.modelformset_factory(
    Designation,
    form=DesignationForm,
    extra=1,
    can_delete=True,
    fields='__all__',
)

IncentiveNameDetailFormSet = forms.modelformset_factory(
    IncentiveName,
    extra=1,
    can_delete=True,
    exclude=('account_category',),
)

EmployeeFacilityFormSet = forms.modelformset_factory(
    EmployeeFacility,
    extra=1,
    can_delete=True,
    fields='__all__'
    # exclude=('account_category',),
)

IncomeTaxSchemeFormSet = forms.inlineformset_factory(
    MaritalStatus,
    IncomeTaxScheme,
    extra=1,
    fields='__all__',
    formset=IncomeTaxSchemeInlineFormSet
)

IncomeTaxCalcSchemeFormSet = forms.inlineformset_factory(
    IncomeTaxScheme,
    IncomeTaxCalcScheme,
    extra=1,
    fields='__all__',
    formset=IncomeTaxCalcSchemeInlineFormSet
)

ReportHrTableFormSet = forms.inlineformset_factory(
    ReportHR,
    ReportTable,
    extra=1,
    exclude=('account',),
    # formset=AllowanceInlineFormset
)


class PayrollConfigForm(HTML5BootstrapModelForm):
    class Meta:
        model = PayrollConfig
        fields = "__all__"


class PayrollAccountantForm(HTML5BootstrapModelForm):
    user = ModelChoiceField(queryset=User.objects.filter(groups__name='Payroll Accountant'), empty_label=None)
    class Meta:
        model = PayrollAccountant
        fields = '__all__'


class BranchOfficeForm(HTML5BootstrapModelForm):

    class Meta:
        model = BranchOffice
        fields = '__all__'


class ProTemporeForm(HTML5BootstrapModelForm):
    class Meta:
        model = ProTempore
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ProTemporeForm, self).clean()
        appoint_date = cleaned_data['appoint_date']
        dismiss_date = cleaned_data['dismiss_date']
        employee = cleaned_data['employee']
        pro_tempore = cleaned_data['employee']
        if employee == pro_tempore:
            raise forms.ValidationError(_('Same employee cannot be assigned as pro tempore.'))
        if dismiss_date < appoint_date:
            raise forms.ValidationError(_('Dismiss date must be greater than appoint date'))

        # # TODO we can do eligibility check as in view(optional)
        # # check whether apoint date is greater than last paid date
        # pro_tempore_last_paid_date = employee_last_payment_record(employee)
        # if pro_tempore_last_paid_date:
        #     if appoint_date != inc_1_day(pro_tempore_last_paid_date):
        #         raise forms.ValidationError(_('Appoint date must be next to last pro tempore paid date'))
        # else:
        #     # TODO check whether from and to of salary is valid time frame
        #     if appoint_date != employee.scale_start_date:
        #         raise forms.ValidationError(_('If employee is never paid appoint date must be employee scale start time.'))


class TaxDeductionForm(HTML5BootstrapModelForm):
    class Meta:
        model = TaxDeduction
        exclude = ('account_category',)



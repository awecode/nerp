import django_filters
from mptt.forms import TreeNodeChoiceField

from hr.fields import HRBSDateFormField
from hr.models import Employee, PayrollEntry, BranchOffice, PayrollConfig
# from hr.filter_forms import EmployeeFilterForm, PayrollEntryFilterForm


class TreeNodeModelChoiceFilter(django_filters.Filter):
    field_class = TreeNodeChoiceField


class HRBSDateFilter(django_filters.Filter):
    fields_class = HRBSDateFormField


class EmployeeFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(EmployeeFilter, self).__init__(*args, **kwargs)

        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.form.fields['working_branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.form.fields['working_branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)
        self.form.fields['working_branch'].empty_label = None

    # is_active = django_filters.BooleanFilter(initial=True)
    working_branch = TreeNodeModelChoiceFilter(
        queryset=BranchOffice.objects.all(),
        help_text='Filter',
    )
    # type = django_filters.ChoiceFilter()

    class Meta:
        model = Employee
        # form = EmployeeFilterForm
        fields = {
            'status': ['exact'],
            'working_branch': ['exact'],
            'type': ['exact']
        }


class PayrollEntryFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(PayrollEntryFilter, self).__init__(*args, **kwargs)

        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.form.fields['branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.form.fields['branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)
        self.form.fields['branch'].empty_label = None


    branch = TreeNodeModelChoiceFilter(
        queryset=BranchOffice.objects.all(),
        help_text='',
    )

    # entry_datetime

    class Meta:
        model = PayrollEntry
        # form = PayrollEntryFilterForm
        fields = {
            'branch': ['exact'],
            # 'entry_datetime': ['exact', 'gte']
        }

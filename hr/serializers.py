from datetime import datetime, date
from njango.middleware import get_calendar
from rest_framework import serializers

from app import settings
from hr.bsdate import BSDate
from hr.helpers import bs_str2tuple
from hr.models import PayrollEntry, PaymentRecord, DeductionDetail, AllowanceDetail, IncentiveDetail, \
    GradeScaleValidity, EmployeeGrade, EmployeeGradeScale, EmployeeGradeGroup, AllowanceValidity, AllowanceName, \
    Allowance, DeductionValidity, Deduction, DeductionName, PayrollConfig, ProTemporeDetail, TaxDetail, ReportHR, ReportTable, ReportTableDetail

from django.utils.translation import ugettext as _


class DeductionDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='deduction.name')
    editable = serializers.ReadOnlyField(source='deduction.amount_editable')

    class Meta:
        model = DeductionDetail
        fields = ('deduction', 'name', 'amount', 'editable', 'amount_added_before_deduction')


class AllowanceDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='allowance.name')

    class Meta:
        model = AllowanceDetail
        fields = ('allowance', 'name', 'amount')


class IncentiveDetailSerializer(serializers.ModelSerializer):
    editable = serializers.ReadOnlyField(source='incentive.amount_editable')
    name = serializers.ReadOnlyField(source='incentive.name')

    class Meta:
        model = IncentiveDetail
        fields = ('incentive', 'name', 'amount', 'editable')


class TaxDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='tax_deduction.name')

    class Meta:
        model = TaxDetail
        fields = ('id', 'name', 'amount')


class ProTemporeDetailSerializer(serializers.ModelSerializer):
    p_t_id = serializers.ReadOnlyField(source='pro_tempore.p_t_id')
    # appoint_date = serializers.ReadOnlyField(source='appoint_date')
    # dismiss_date = serializers.ReadOnlyField(source='dismiss_date')
    employee_name = serializers.ReadOnlyField(source='pro_tempore.employee.name')
    employee_designation = serializers.ReadOnlyField(source='pro_tempore.employee.designation.designation_name')

    class Meta:
        model = ProTemporeDetail
        fields = ('p_t_id', 'amount', 'appoint_date', 'dismiss_date', 'employee_name', 'employee_designation')


class PaymentRecordSerializer(serializers.ModelSerializer):
    incentive_details = IncentiveDetailSerializer(many=True)
    allowance_details = AllowanceDetailSerializer(many=True)
    deduction_details = DeductionDetailSerializer(many=True)
    pro_tempore_details = ProTemporeDetailSerializer(many=True)
    tax_details = TaxDetailSerializer(many=True)
    # is_explicitly_added_row = serializers.SerializerMethodField('explicitly_added')
    paid_employee = serializers.SerializerMethodField('get_paid_employee_as_str')

    employee_grade = serializers.ReadOnlyField(source='paid_employee.designation.grade.grade_name')
    employee_designation = serializers.ReadOnlyField(source='paid_employee.designation.designation_name')

    paid_from_date = serializers.CharField(max_length=50)
    paid_to_date = serializers.CharField(max_length=50)

    class Meta:
        model = PaymentRecord
        fields = '__all__'

    # def explicitly_added(self, instance):
    #     return False

    def get_paid_employee_as_str(self, instance):
        return str(instance.paid_employee.id)


class PayrollEntrySerializer(serializers.ModelSerializer):
    entry_rows = PaymentRecordSerializer(many=True)
    computed_scenario = serializers.SerializerMethodField('get_scenario')
    branch = serializers.SerializerMethodField('get_branch_value')
    paid_from_date_input = serializers.SerializerMethodField('get_from_date')
    paid_to_date_input = serializers.SerializerMethodField('get_to_date')
    entry_date = serializers.SerializerMethodField()

    class Meta:

        model = PayrollEntry
        # fields = '__all__'
        exclude = ('paid_from_date', 'paid_to_date')
        include = ('entry_saved', 'paid_from_date_input', 'paid_to_date_input', 'entry_date', 'entry_rows')

    # either edit True or False
    def get_scenario(self, instance):
        if instance.id == PayrollEntry.objects.order_by('-id').values('id').first().get('id'):
            return 'EDIT'
        else:
            return 'DETAIL-VIEW'

    def get_from_date(self, instance):
        if isinstance(instance.paid_from_date, date):
            return str(instance.paid_from_date)
        else:
            return instance.paid_from_date.as_string()

    def get_to_date(self, instance):
        if isinstance(instance.paid_to_date, date):
            return str(instance.paid_to_date)
        else:
            return instance.paid_to_date.as_string()

    def get_entry_date(self, instance):
        if isinstance(instance.entry_date, date):
            return str(instance.entry_date)
        else:
            return instance.entry_date.as_string()

    def get_branch_value(self, instance):
        if not instance.branch:
            return 'ALL'
        else:
            return instance.branch.id


class GradeScaleValiditySerializer(serializers.ModelSerializer):
    valid_from = serializers.CharField()

    class Meta:
        model = GradeScaleValidity
        fields = ('id', 'valid_from', 'note')

    def validate_valid_from(self, value):
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        if HR_CALENDAR == 'AD':
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except:
                raise serializers.ValidationError(_('Invalid AD date. Date format: YYYY-MM-DD '))
        else:
            try:
                BSDate(*bs_str2tuple(value))
            except:
                raise serializers.ValidationError(_('Invalid BS date. Date format: YYYY-MM-DD '))
        return value

    def validate(self, data):
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        valid_from = data['valid_from']

        available_validities = GradeScaleValidity.objects.all()

        if HR_CALENDAR == 'AD':
            valid_from = datetime.strptime(valid_from, '%Y-%m-%d')
            for validity in available_validities:
                if valid_from < validity.valid_from:
                    raise serializers.ValidationError(_('New validity must be greater than previous validity'))
        else:
            valid_from = BSDate(*bs_str2tuple(valid_from))
            for validity in available_validities:
                if valid_from < validity.valid_from:
                    raise serializers.ValidationError(_('New validity must be greater than previous validity'))
        return data


class EmployeeGradeScaleSerializer(serializers.ModelSerializer):
    grade_id = serializers.ReadOnlyField(source="grade.id")
    validity_id = serializers.ReadOnlyField(source="validity.id")

    # parent_grade_id = serializers.ReadOnlyField(source="grade.group.id")
    # # parent_grade_name = serializers.ReadOnlyField(source="grade.group.name")

    class Meta:
        model = EmployeeGradeScale
        fields = (
            'id',
            'grade_id',
            'salary_scale',
            'grade_number',
            'grade_rate',
            'validity_id',

            # # Non model fields
            # 'grade_name',
            # 'parent_grade_id',
            # 'parent_grade_name'
        )


class EmployeeGradeSerializer(serializers.ModelSerializer):
    # grade_scales = EmployeeGradeScaleSerializer(many=True)
    # grade_group_id = serializers.ReadOnlyField(source="grade_group.id")
    class Meta:
        model = EmployeeGrade
        fields = ('id', 'grade_name', 'grade_group')


class EmployeeGradeGroupSerializer(serializers.ModelSerializer):
    employee_grades = EmployeeGradeSerializer(many=True)

    class Meta:
        model = EmployeeGradeGroup
        fields = ('id', 'name', 'employee_grades')


# Allowance

class AllowanceValiditySerializer(serializers.ModelSerializer):
    valid_from = serializers.CharField()

    class Meta:
        model = AllowanceValidity
        fields = ('id', 'valid_from', 'note')

    def validate_valid_from(self, value):
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        if HR_CALENDAR == 'AD':
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except:
                raise serializers.ValidationError(_('Invalid AD date. Date format: YYYY-MM-DD '))
        else:
            try:
                BSDate(*bs_str2tuple(value))
            except:
                raise serializers.ValidationError(_('Invalid BS date. Date format: YYYY-MM-DD '))
        return value

    def validate(self, data):
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        valid_from = data['valid_from']

        available_validities = AllowanceValidity.objects.all()

        if HR_CALENDAR == 'AD':
            valid_from = datetime.strptime(valid_from, '%Y-%m-%d')
            for validity in available_validities:
                if valid_from < validity.valid_from:
                    raise serializers.ValidationError(_('New validity must be greater than previous validity'))
        else:
            valid_from = BSDate(*bs_str2tuple(valid_from))
            for validity in available_validities:
                if valid_from < validity.valid_from:
                    raise serializers.ValidationError(_('New validity must be greater than previous validity'))
        return data


class AllowanceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowanceName
        fields = '__all__'


class AllowanceSerializer(serializers.ModelSerializer):
    employee_grade_id = serializers.ReadOnlyField(source='employee_grade.id')
    validity_id = serializers.ReadOnlyField(source='validity.id')
    name_id = serializers.ReadOnlyField(source='name.id')

    class Meta:
        model = Allowance
        fields = (
            'id',
            'name_id',
            'employee_grade_id',
            'sum_type',
            'value',
            'payment_cycle',
            'year_payment_cycle_month',
            'validity_id'
        )


# End Allowance


# Deduction
class DeductionValiditySerializer(serializers.ModelSerializer):
    valid_from = serializers.CharField()

    class Meta:
        model = DeductionValidity
        fields = ('id', 'valid_from', 'note')

    def validate_valid_from(self, value):
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        if HR_CALENDAR == 'AD':
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except:
                raise serializers.ValidationError(_('Invalid AD date. Date format: YYYY-MM-DD '))
        else:
            try:
                BSDate(*bs_str2tuple(value))
            except:
                raise serializers.ValidationError(_('Invalid BS date. Date format: YYYY-MM-DD '))
        return value

    def validate(self, data):
        HR_CALENDAR = PayrollConfig.get_solo().hr_calendar
        valid_from = data['valid_from']

        available_validities = DeductionValidity.objects.all()

        if HR_CALENDAR == 'AD':
            valid_from = datetime.strptime(valid_from, '%Y-%m-%d')
            for validity in available_validities:
                if valid_from < validity.valid_from:
                    raise serializers.ValidationError(_('New validity must be greater than previous validity'))
        else:
            valid_from = BSDate(*bs_str2tuple(valid_from))
            for validity in available_validities:
                if valid_from < validity.valid_from:
                    raise serializers.ValidationError(_('New validity must be greater than previous validity'))
        return data


class DeductionNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeductionName
        fields = '__all__'


class DeductionSerializer(serializers.ModelSerializer):
    validity_id = serializers.ReadOnlyField(source="validity.id")
    name_id = serializers.ReadOnlyField(source="name.id")

    class Meta:
        model = Deduction
        fields = (
            'id',
            'name_id',
            'deduct_type',
            'value',
            'validity_id'
        )
        # End Deduction


class ReportTableDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTableDetail
        fields = (
            'id',
            'field_name',
            'field_description',
            'order',
            'need_total'
            )


class ReportTableSerializer(serializers.ModelSerializer):
    table_details = ReportTableDetailSerializer(many=True)

    class Meta:
        model = ReportTable
        fields = (
            'id',
            'title',
            'table_details'
            )


class ReportHRSerializer(serializers.ModelSerializer):

    report_tables = ReportTableSerializer(many=True)

    class Meta:
        model = ReportHR
        fields = (
            'id',
            'name',
            'code',
            'template',
            # 'for_employee_type',
            'report_tables'
            )
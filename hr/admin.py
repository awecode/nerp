from django.contrib import admin
from import_export import resources

from .models import EmployeeAccount, EmployeeGrade, Employee, Designation, Incentive, Allowance, IncomeTaxScheme, \
    BranchOffice, Deduction, ProTempore, PaymentRecord, PayrollEntry, IncentiveName, AllowanceName, DeductionDetail, \
    IncentiveDetail, AllowanceDetail, MaritalStatus, \
    ReportTable, ReportHR, GradeScaleValidity, EmployeeGradeScale, DeductionValidity, AllowanceValidity, \
    PayrollAccountant, PayrollConfig, DeductionName, TaxDetail, TaxDeduction, ReportTableDetail, Bank
from .forms import EmployeeAccountInlineFormset, AllowanceForm, IncentiveForm, DeductionForm, EmployeeForm, \
    IncentiveInlineFormset
from solo.admin import SingletonModelAdmin

class EmployeeAccountInline(admin.TabularInline):
    model = EmployeeAccount
    formset = EmployeeAccountInlineFormset
    extra = 1


class EmployeeIncentiveInline(admin.TabularInline):
    model = Incentive
    formset = IncentiveInlineFormset
    extra = 1


class EmployeeAdmin(admin.ModelAdmin):
    inlines = (EmployeeAccountInline, EmployeeIncentiveInline)
    form = EmployeeForm
    pass


class AllowanceAdmin(admin.ModelAdmin):
    form = AllowanceForm


class IncentiveAdmin(admin.ModelAdmin):
    form = IncentiveForm


class DeductionAdmin(admin.ModelAdmin):
    form = DeductionForm


# Django Import Export Resource Class

class EmployeeImportResource(resources.ModelResource):
    class Meta:
        model = Employee


# End Django Import Export Resource Class

admin.site.register(EmployeeGrade)

admin.site.register(PayrollAccountant)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Designation)
admin.site.register(Incentive, IncentiveAdmin)
admin.site.register(Allowance, AllowanceAdmin)
admin.site.register(IncomeTaxScheme)
admin.site.register(BranchOffice)
admin.site.register(Deduction, DeductionAdmin)
admin.site.register(DeductionName)
admin.site.register(ProTempore)
admin.site.register(PaymentRecord)
admin.site.register(PayrollEntry)
admin.site.register(EmployeeAccount)
admin.site.register(IncentiveName)
admin.site.register(AllowanceName)

admin.site.register(Bank)

admin.site.register(DeductionDetail)
admin.site.register(IncentiveDetail)
admin.site.register(AllowanceDetail)
admin.site.register(TaxDetail)
admin.site.register(TaxDeduction)

# admin.site.register(AllowanceAccount)
# admin.site.register(IncentiveAccount)
# admin.site.register(DeductionAccount)
# admin.site.register(JournalEntry)
# admin.site.register(CompanyAccount)
admin.site.register(MaritalStatus)
admin.site.register(ReportHR)
admin.site.register(ReportTable)
admin.site.register(ReportTableDetail)
admin.site.register(GradeScaleValidity)
admin.site.register(DeductionValidity)
admin.site.register(AllowanceValidity)
admin.site.register(EmployeeGradeScale)
# admin.site.register(SalaryAccount)

admin.site.register(PayrollConfig, SingletonModelAdmin)
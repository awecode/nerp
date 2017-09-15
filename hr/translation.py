from modeltranslation.translator import translator, TranslationOptions
from app.utils.translation import NameTranslationOptions
from hr.models import Employee, DeductionName, BranchOffice, IncentiveName, AllowanceName, Designation, \
    EmployeeGradeGroup, EmployeeGrade, TaxDeduction, ReportHR, EmployeeFacility, ReportTableDetail, ReportTable, Bank, \
    PayrollConfig


class DesignationTranslationOptions(TranslationOptions):
    fields = ('designation_name',)


class EmployeeGradeTranslationOptions(TranslationOptions):
    fields = ('grade_name',)


class ReportTableTranslationOption(TranslationOptions):
    fields = ('title',)


class ReportTableDetailTranslationOption(TranslationOptions):
    fields = ('field_name',)


class BranchOfficeTranslationOptions(TranslationOptions):
    fields = ('name', 'address')

class PayrollConfigTranslationOptions(TranslationOptions):
    fields = ('organization_title',)

translator.register(Employee, NameTranslationOptions)
translator.register(DeductionName, NameTranslationOptions)
translator.register(BranchOffice, BranchOfficeTranslationOptions)
translator.register(IncentiveName, NameTranslationOptions)
translator.register(AllowanceName, NameTranslationOptions)
translator.register(EmployeeGradeGroup, NameTranslationOptions)
translator.register(Designation, DesignationTranslationOptions)
translator.register(EmployeeGrade, EmployeeGradeTranslationOptions)
translator.register(TaxDeduction, NameTranslationOptions)
translator.register(ReportHR, NameTranslationOptions)
translator.register(EmployeeFacility, NameTranslationOptions)
translator.register(Bank, NameTranslationOptions)

translator.register(ReportTable, ReportTableTranslationOption)
translator.register(ReportTableDetail, ReportTableDetailTranslationOption)

translator.register(PayrollConfig, PayrollConfigTranslationOptions)
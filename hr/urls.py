from django.conf.urls import patterns, url, include
from django.views.i18n import javascript_catalog
from rest_framework.routers import DefaultRouter

import views
import api

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'grade-scale', api.EmployeeGradeScaleViewSet)
router.register(r'grade-group', api.EmployeeGradeGroupViewSet)
router.register(r'grade-scale-validity', api.GradeScaleValidityViewSet)
router.register(r'employee-grade', api.EmployeeGradeViewSet)

# Allowance Routers
router.register(r'allowance-validity', api.AllowanceValidityViewSet)
router.register(r'allowance-name', api.AllowanceNameViewSet)
router.register(r'allowance', api.AllowanceViewSet)
# End Allowance Routers

# Deduction Routers
router.register(r'deduction-validity', api.DeductionValidityViewSet)
router.register(r'deduction', api.DeductionViewSet)
router.register(r'deduction-name', api.DeductionNameViewSet)
# End Deduction Routers

js_info_dict = {
    'packages': ('hr',),
}

urlpatterns = patterns('',
                       url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
                       url(r'^api/', include(router.urls)),
                       # url(r'^api/', include('rest_framework.urls', namespace='hr-api')),
                       url(r'^$', views.payroll_index, name='payroll_index'),
                       url(r'^entry/$', views.payroll_entry, name='payroll_entry'),
                       url(r'^entry/(?P<pk>[0-9]+)/$', views.payroll_entry, name='payroll_entry_edit'),
                       url(r'^get_employee_account/$', views.get_employee_account, name='get_employee_account'),
                       url(r'^get_employees_account/$', views.get_employees_account, name='get_employees_account'),
                       url(r'^save_payroll_entry/$', views.save_payroll_entry, name='save_payroll_entry'),
                       url(r'^save_payroll_entry/(?P<pk>[0-9]+)/$', views.save_payroll_entry,
                           name='save_payroll_entry_edit'),
                       url(r'^entry_detail/(?P<pk>[0-9]+)/$', views.entry_detail, name='entry_detail'),
                       url(r'^entry_list/$', views.entry_list, name='entry_list'),
                       url(r'^get_employee_options/$', views.get_employee_options, name='get_employee_options'),
                       url(r'^approve_entry/(?P<pk>[0-9]+)/$', views.approve_entry, name='approve_entry'),
                       url(r'^transact_entry/(?P<pk>[0-9]+)/$', views.transact_entry, name='transact_entry'),
                       url(r'^delete_entry/(?P<pk>[0-9]+)/$', views.delete_entry, name='delete_entry'),

                       # employee crud
                       url(r'^employee/add/$', views.employee, name='add_employee'),
                       url(r'^employee/edit/(?P<pk>[0-9]+)/$', views.employee, name='edit_employee'),
                       # url(r'^employee/toggle_activeness/(?P<pk>[0-9]+)/$', views.toggle_employee_activeness,
                       #     name='toggle_employee_activeness'),
                       url(r'^employee/list/$', views.list_employee, name='list_employee'),

                       # # incentive crud
                       # url(r'^incentive/add/$', views.incentive, name='add_incentive'),
                       # url(r'^incentive/edit/(?P<pk>[0-9]+)/$', views.incentive, name='edit_incentive'),
                       # url(r'^incentive/delete/(?P<pk>[0-9]+)/$', views.delete_incentive, name='delete_incentive'),
                       # url(r'^incentive/list/$', views.list_incentive, name='list_incentive'),

                       # allowance crud
                       url(r'^allowance-entry/$', views.allowance, name='add_allowance'),

                       # deductions crud

                       url(r'^deduction-entry/$', views.deduction, name='deduction'),

                       url(r'^deduction-name/$', views.deduction_name, name='deduction_name'),

                       # Employee Grade
                       url(r'^employee-grade-group/$', views.employee_grade_group, name='employee_grade_group'),
                       url(r'^employee-grade/$', views.employee_grade, name='employee_grade'),

                       # Employee Designation
                       url(r'^designations/$', views.employee_designation, name='employee_designation'),

                       # incentivenames crud
                       url(r'^incentives/$', views.incentivename_curd, name='incentivename_curd'),

                       # facility crud
                       url(r'^employee-facilities/$', views.facility_curd, name='facility_curd'),

                       # taxation crud
                       # url(r'^tax/scheme/$', views.tax_scheme, name='tax_scheme'),

                       # tax_detail_scheme crud
                       url(r'^taxschemedetail/add/$', views.tax_scheme_detail, name='add_tax_scheme'),
                       url(r'^taxschemedetail/edit/(?P<pk>[0-9]+)/$', views.tax_scheme_detail, name='edit_tax_scheme'),
                       # url(r'^taxschemedetail/delete/(?P<pk>[0-9]+)/$', views.delete_tax_scheme, name='delete_tax_scheme'),
                       url(r'^taxscheme/list/$', views.list_tax_scheme, name='list_tax_scheme'),

                       # tax_scheme crud
                       url(r'^taxscheme/add/$', views.tax_scheme, name='add_taxscheme'),
                       url(r'^taxscheme/edit/(?P<pk>[0-9]+)/$', views.tax_scheme, name='edit_taxscheme'),
                       url(r'^taxscheme/delete/(?P<pk>[0-9]+)/$', views.delete_taxscheme, name='delete_taxscheme'),

                       # url(r'^taxscheme/list/$', views.list_tax_scheme, name='list_tax_scheme'),
                       # url(r'^allowance/edit/(?P<pk>[0-9]+)/$', views.allowance, name='edit_allowance'),
                       # url(r'^by_branch/$', views.group_payroll_branch, name='group_payroll_branch'),
                       url(r'^report/$', views.get_report, name='get_report'),
                       # url(r'^generate_report/$', views.generate_report, name='generate_report'),

                       # report setting crud
                       url(r'^report-setting/add/$', views.report_setting, name='add_report_setting'),
                       url(r'^report-setting/edit/(?P<pk>[0-9]+)/$', views.report_setting, name='edit_report_setting'),
                       url(r'^report-setting/delete/(?P<pk>[0-9]+)/$', views.delete_report_setting,
                           name='delete_report_setting'),
                       url(r'^report-setting/list/$', views.list_report_setting, name='list_report_setting'),

                       # GradeScale
                       url(r'^grades-scale-entry/$', views.grades_scale, name='grade-scale-entry'),
                       # EndGradeScale

                       # Payroll Configuration
                       url(r'^config/$', views.PayrollConfigUpdateView.as_view(), name='payroll_config'),
                       # End Payroll Configuration

                       # Branch Accounant Crud
                       url(r'^accountant/add/$', views.PayrollAccountantCreate.as_view(),
                           name='payroll_accountant_add'),
                       url(r'^accountant/edit/(?P<pk>[0-9]+)/$', views.PayrollAccountantUpdate.as_view(),
                           name='payroll_accountant_edit'),
                       url(r'^accountant/list/$', views.PayrollAccountantList.as_view(),
                           name='payroll_accountant_list'),
                       url(r'^accountant/delete/(?P<pk>[0-9]+)/$', views.PayrollAccountantDelete.as_view(),
                           name='payroll_accountant_delete'),
                       # End Branch Accounant Crud

                       # Branch Office Crud
                       url(r'^branch/add/$', views.BranchCreate.as_view(),
                           name='branch_add'),
                       url(r'^branch/edit/(?P<pk>[0-9]+)/$', views.BranchUpdate.as_view(),
                           name='branch_edit'),
                       url(r'^branch/list/$', views.BranchList.as_view(),
                           name='branch_list'),
                       url(r'^branch/delete/(?P<pk>[0-9]+)/$', views.BranchDelete.as_view(),
                           name='branch_delete'),
                       # End Branch Office Crud

                       # Pro Tempore Crud
                       url(r'^protempore/add/$', views.ProTemporeCreate.as_view(),
                           name='protempore_add'),
                       url(r'^protempore/edit/(?P<pk>[0-9]+)/$', views.ProTemporeUpdate.as_view(),
                           name='protempore_edit'),
                       url(r'^protempore/list/$', views.ProTemporeList.as_view(),
                           name='protempore_list'),
                       url(r'^protempore/delete/(?P<pk>[0-9]+)/$', views.ProTemporeDelete.as_view(),
                           name='protempore_delete'),
                       # End ProTempore Crud

                       # TaxDeduction Crud
                       url(r'^taxdeduction/add/$', views.TaxDeductionCreate.as_view(),
                           name='taxdeduction_add'),
                       url(r'^taxdeduction/edit/(?P<pk>[0-9]+)/$', views.TaxDeductionUpdate.as_view(),
                           name='taxdeduction_edit'),
                       url(r'^taxdeduction/list/$', views.TaxDeductionList.as_view(),
                           name='taxdeduction_list'),
                       url(r'^taxdedution/delete/(?P<pk>[0-9]+)/$', views.TaxDeductionDelete.as_view(),
                           name='taxdeduction_delete'),
                       # End ProTempore Crud

                       url(r'^get-report-field/$', views.get_report_field_options,
                           name='get-report-field'),
                       url(r'^get-selected-options/$', views.load_selected_options,
                           name='get-selected-options'),
                       )

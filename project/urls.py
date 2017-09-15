from django.conf.urls import url

import views

urlpatterns = [

    url(r'^$', views.index, name='project_index'),
    url(r'^(?P<project_fy_id>[0-9]+)/account/(?P<account_id>[0-9]+)/$', views.ImprestLedger.as_view(), name='account_view'),
    url(r'^(?P<project_fy_id>[0-9]+)/application/$', views.Application.as_view(), name='application'),
    url(r'^application/save/$', views.save_application, name='save_application'),

    url(r'^(?P<project_fy_id>[0-9]+)/journal_vouchers/$', views.ImprestJVList.as_view(), name='imprest_journal_voucher_list'),
    url(r'^(?P<project_fy_id>[0-9]+)/journal_voucher/$', views.ImprestJVCreate.as_view(), name='imprest_journal_voucher_add'),
    url(r'^(?P<project_fy_id>[0-9]+)/journal_voucher/(?P<pk>\d+)/$', views.ImprestJVUpdate.as_view(),
        name='imprest_journal_voucher_edit'),
    url(r'^(?P<project_fy_id>[0-9]+)/journal_voucher/(?P<pk>\d+)/delete/$', views.ImprestJVDelete.as_view(),
        name='imprest_journal_voucher_delete'),
    url(r'^(?P<project_fy_id>[0-9]+)/ledgers/$', views.ledgers,
        name='ledger_list'),

    url(r'^(?P<project_id>[0-9]+)/aids/$', views.AidList.as_view(), name='aid_list'),
    url(r'^(?P<project_id>[0-9]+)/aid/add/$', views.AidCreate.as_view(), name='aid_add'),
    url(r'^(?P<project_id>[0-9]+)/aid/edit/(?P<pk>\d+)/$', views.AidUpdate.as_view(),
        name='aid_edit'),
    url(r'^(?P<project_id>[0-9]+)/aid/delete/(?P<pk>\d+)/$', views.AidDelete.as_view(),
        name='aid_delete'),

    url(r'^projects/$', views.ProjectList.as_view(), name='project_list'),
    url(r'^project/add/$', views.ProjectCreate.as_view(), name='project_add'),
    url(r'^project/edit/(?P<pk>\d+)/$', views.ProjectUpdate.as_view(),
        name='project_edit'),
    url(r'^project/delete/(?P<pk>\d+)/$', views.ProjectDelete.as_view(),
        name='project_delete'),

    url(r'^(?P<project_id>[0-9]+)/expense_categories/$', views.ExpenseCategoryList.as_view(), name='expense_category_list'),
    url(r'^(?P<project_id>[0-9]+)/expense_category/add/$', views.ExpenseCategoryCreate.as_view(),
        name='expense_category_add'),
    url(r'^(?P<project_id>[0-9]+)/expense_category/edit/(?P<pk>\d+)/$', views.ExpenseCategoryUpdate.as_view(),
        name='expense_category_edit'),
    url(r'^(?P<project_id>[0-9]+)/expense_category/delete/(?P<pk>\d+)/$', views.ExpenseCategoryDelete.as_view(),
        name='expense_category_delete'),

    url(r'^(?P<project_id>[0-9]+)/expenses/$', views.ExpenseList.as_view(), name='expense_list'),
    url(r'^(?P<project_id>[0-9]+)/expense/add/$', views.ExpenseCreate.as_view(),
        name='expense_add'),
    url(r'^(?P<project_id>[0-9]+)/expense/edit/(?P<pk>\d+)/$', views.ExpenseUpdate.as_view(),
        name='expense_edit'),
    url(r'^(?P<project_id>[0-9]+)/expense/delete/(?P<pk>\d+)/$', views.ExpenseDelete.as_view(),
        name='expense_delete'),

    url(r'^(?P<project_fy_id>[0-9]+)/budget_allocation/$', views.BudgetAllocation.as_view(),
        name='budget_allocation'),
    url(r'^budget_allocation/save/$', views.save_budget_allocation,
        name='save_budget_allocation'),

    url(r'^(?P<project_fy_id>[0-9]+)/budget_release/$', views.BudgetRelease.as_view(),
        name='budget_release'),
    url(r'^budget_release/save/$', views.save_budget_release,
        name='save_budget_release'),

    url(r'^(?P<project_fy_id>[0-9]+)/expenditure/$', views.BudgetExpenditure.as_view(),
        name='budget_expenditure'),
    url(r'^expenditure/save/$', views.save_expenditure,
        name='save_expenditure'),
    url(r'^(?P<project_fy_id>[0-9]+)/reimbursement/$', views.ReimbursementList.as_view(),
        name='reimbursement_list'),
    url(r'^(?P<project_fy_id>[0-9]+)/reimbursement/add/$', views.ReimbursementCreate.as_view(),
        name='reimbursement_add'),
    url(r'^(?P<project_fy_id>[0-9]+)/reimbursement/(?P<pk>[0-9]+)/$', views.ReimbursementUpdate.as_view(),
        name='reimbursement_edit'),
    url(r'^(?P<project_fy_id>[0-9]+)/reimbursement/delete/(?P<pk>[0-9]+)/$', views.ReimbursementDelete.as_view(),
        name='reimbursement_delete'),

    url(r'^(?P<project_fy_id>[0-9]+)/statement_of_funds/$', views.statement_of_fund_template,
        name='statement_of_funds'),

    url(r'^(?P<project_fy_id>[0-9]+)/memorandum_statement/$', views.memorandum_statement,
        name='memorandum_statement'),

    url(r'^(?P<project_fy_id>[0-9]+)/aid_disbursement/$', views.aid_disbursement,
        name='aid_disbursement'),

    url(r'^(?P<project_fy_id>[0-9]+)/disbursement_details/$', views.DisbursementDetailList.as_view(), name='disbursement_detail_list'),
    url(r'^(?P<project_fy_id>[0-9]+)/disbursement_detail/$', views.DisbursementDetailCreate.as_view(), name='disbursement_detail_add'),
    url(r'^(?P<project_fy_id>[0-9]+)/disbursement_detail/(?P<pk>\d+)/$', views.DisbursementDetailCreate.as_view(),
        name='disbursement_detail_edit'),
    url(r'^(?P<project_fy_id>[0-9]+)/disbursement_detail/delete/(?P<pk>\d+)/$', views.DisbursementDetailDelete.as_view(),
        name='disbursement_detail_delete'),
    url(r'^disbursement_detail/save/$', views.save_disbursement_detail, name='save_save_disbursement_detail'),


]

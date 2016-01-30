from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='inventory_index'),
                       url(r'^yearly_report/$', views.yearly_report_list, name='yearly_report_list'),
                       url(r'^yearly_report/create$', views.yearly_report, name='yearly_report'),
                       url(r'^save/yearly_report/$', views.save_yearly_report, name='save_yearly_report'),
                       url(r'^save/yearly_report_detail/$', views.save_yearly_report_detail, name='save_yearly_report_detail'),
                       url(r'^yearly_report/(?P<id>[0-9]+)/$', views.yearly_report_detail, name='yearly_report_detail'),
                       url(r'^yearly_report/(?P<id>[0-9]+)/delete$', views.delete_yearly_report,
                           name='delete_yearly_report'),
                       url(r'^transactions/$', views.list_transactions, name='inventory_transactions_list'),
                       url(r'^iteminstance/(?P<id>[0-9]+)/$', views.item_instance_form,
                           name='item_instance_detail'),
                       url(r'^quotation/list$', views.quotation_report_list, name='list_quotation_forms'),
                       url(r'^quotation/detail/(?P<id>[0-9]+)/$', views.quotation_report, name='detail_quotation_forms'),
                       url(r'^quotation/create$', views.quotation_report, name='quotation_report'),
                       url(r'^quotations/(?P<id>[0-9]+)/delete$', views.delete_quotation_comparison,
                           name='delete_quotation_comparison'),
                       url(r'^inspection/$', views.inspection_report_list, name='inspection_report_list'),
                       url(r'^save/inspection/$', views.save_inspection_report, name='save_inspection_report'),
                       url(r'^inspection/create$', views.inspection_report, name='inspection_report'),
                       url(r'^inspection/(?P<id>[0-9]+)/$', views.inspection_report_detail, name='inspection_report_detail'),
                       url(r'^inspection/(?P<id>[0-9]+)/delete$', views.delete_inspection_report,
                           name='delete_inspection_report'),
                       url(r'^save/quotation-comparison/$', views.save_quotation_comparison, name='save_quotation_comparison'),

                       url(r'^items/$', views.list_inventory_items, name='list_inventory_items'),
                       url(r'^create/$', views.item_form, name='create_inventory_item'),
                       url(r'^item/delete/(?P<id>[0-9]+)/$', views.delete_inventory_item, name='delete_inventory_item'),
                       url(r'^(?P<id>[0-9]+)/$', views.item_form, name='update_inventory_item'),
                       url(r'^items.json$', views.items_as_json, name='items_as_json'),
                       url(r'^item_instances.json$', views.item_instances_as_json, name='item_instances_as_json'),
                       url(r'^items_locations.json$', views.items_locations_as_json, name='get_items_locations'),
                       url(r'^create_item_location$', views.create_item_location, name='create_item_location'),
                       url(r'^il/(?P<id>[0-9]+)/$', views.create_item_location, name='update_item_location'),

                       url(r'^accounts/$', views.list_inventory_accounts, name='list_inventory_accounts'),
                       url(r'^accounts/consumable/$', views.list_consumable_accounts,
                           name='list_consumable_inventory_accounts'),
                       url(r'^accounts/non-consumable/$', views.list_non_consumable_accounts,
                           name='list_non_consumable_inventory_accounts'),
                       url(r'^account/(?P<id>[0-9]+)/$', views.view_inventory_account, name='view_inventory_account'),
                       url(r'^account/(?P<id>[0-9]+)/(?P<year>[0-9]{4})/$', views.view_inventory_account,
                           name='view_inventory_account_by_year'),
                       url(r'^save/account/$', views.save_account, name='save_inventory_account'),

                       url(r'^categories/$', views.list_categories, name='list_inventory_categories'),
                       url(r'^category/create/$', views.create_category, name='create_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category,
                           name='delete_inventory_category'),

                       url(r'^demand/$', views.demand_form, name='create_demand_form'),
                       url(r'^demand/(?P<id>[0-9]+)/$', views.demand_form, name='update_demand_form'),
                       url(r'^save/demand_form/$', views.save_demand, name='save_demand_form'),
                       url(r'^approve/demand_form/$', views.approve_demand, name='approve_demand_form'),
                       url(r'^fulfill/demand_form/$', views.fulfill_demand, name='fulfill_demand_form'),
                       url(r'^disapprove/demand_form/$', views.disapprove_demand, name='disapprove_demand_form'),
                       url(r'^unfulfill/demand_form/$', views.unfulfill_demand, name='unfulfill_demand_form'),
                       url(r'^demand/(?P<id>[0-9]+)/delete$', views.delete_demand,
                           name='delete_demand_form'),
                       url(r'^demand/(?P<id>[0-9]+)/xls-demandform-converter$', views.convert_demand,
                           name='convert_demand_form'),

                       url(r'^demand-forms/$', views.list_demand_forms, name='list_demand_forms'),

                       url(r'^handovers/$', views.list_handovers, name='list_handovers'),
                       url(r'^handover/incoming/$', views.handover_incoming, name='create_incoming_handover'),
                       url(r'^handover/outgoing/$', views.handover_outgoing, name='create_outgoing_handover'),
                       url(r'^save/handover/$', views.save_handover, name='save_handover'),
                       url(r'^handover/(?P<id>[0-9]+)/$', views.handover_incoming, name='update_handover'),
                       url(r'^handovers/incoming/$', views.list_incoming_handovers, name='list_incoming_handovers'),
                       url(r'^handovers/outgoing/$', views.list_outgoing_handovers, name='list_outgoing_handovers'),
                       url(r'^handover/(?P<id>[0-9]+)/delete$', views.delete_handover,
                           name='delete_handover'),

                       url(r'^purchase-order/$', views.purchase_order, name='create_purchase_order'),
                       url(r'^purchase-order/(?P<id>[0-9]+)/$', views.purchase_order, name='update_purchase_order'),
                       url(r'^save/purchase_order/$', views.save_purchase_order, name='save_purchase_order'),
                       url(r'^purchase-order/(?P<id>[0-9]+)/delete$', views.delete_purchase_order,
                           name='delete_purchase_order'),
                       url(r'^purchase-order/(?P<id>[0-9]+)/xls-demandform-converter$', views.convert_purchase_order,
                           name='convert_purchase_order'),

                       url(r'^purchase-orders/$', views.list_purchase_orders, name='list_purchase_orders'),
                       url(r'^entry-report/(?P<id>[0-9]+)/xls-demandform-converter$', views.convert_entry_report,
                           name='convert_entry_report'),

                       url(r'^entry-report/handover/(?P<id>[0-9]+)/$', views.handover_entry_report,
                           name='handover_entry_report'),
                       url(r'^entry-report/purchase/(?P<id>[0-9]+)/$', views.purchase_entry_report,
                           name='purchase_entry_report'),
                       url(r'^save/entry_report/$', views.save_entry_report, name='save_entry_report'),
                       url(r'^delete-entry-report/(?P<id>[0-9]+)/delete$', views.delete_entry_report,
                           name='delete_entry_report'),
                       url(r'^entry-reports/$', views.list_entry_reports, name='list_entry_reports'),
                       url(r'^entry-reports/handover/$', views.list_handover_entry_reports,
                           name='list_handover_entry_reports'),
                       url(r'^entry-reports/purchase/$', views.list_purchase_entry_reports,
                           name='list_purchase_entry_reports'),
                       url(r'^depreciation-report/$', views.depreciation_report,
                           name='depreciation_report'),

                       url(r'^locations/$', views.LocationList.as_view(),
                           name='itemlocation_list'),
                       url(r'^locations/(?P<pk>[0-9]+)$', views.LocationDetail.as_view(),
                           name='itemlocation_detail'),

                       url(r'^user_ledgers/$', views.user_ledgers, name='user_ledger_list'),
                       url(r'^user_ledger/(?P<pk>[0-9]+)/$', views.user_ledger_detail, name='user_ledger_detail'),

                       url(r'^instance/(?P<pk>[0-9]+)/$', views.ItemInstanceView.as_view(), name='iteminstance_form'),

                       url(r'^history/(?P<instance_pk>[0-9]+)/$', views.InstanceHistoryView.as_view(),
                           name='iteminstance_history'),

                       url(r'^return/(?P<pk>[0-9]+)/$', views.return_to_store, name='return_to_store'),

                       url(r'^instance/(?P<instance_pk>[0-9]+)/expense/$', views.ExpenseCreate.as_view(),
                           name='iteminstance_expense'),

                       # url(r'^expense/(?P<pk>[0-9]+)/$', views.ExpenseCreate.as_view(), name='expense_update'),

                       url(r'^ledgers.pdf$', views.LedgersPDFView.as_view())

                       )

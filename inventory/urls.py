from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='inventory_index'),

                       url(r'^items/$', views.list_inventory_items, name='list_inventory_items'),
                       url(r'^create/$', views.item_form, name='create_inventory_item'),
                       url(r'^item/delete/(?P<id>[0-9]+)/$', views.delete_inventory_item, name='delete_inventory_item'),
                       url(r'^(?P<id>[0-9]+)/$', views.item_form, name='update_inventory_item'),
                       url(r'^items.json$', views.items_as_json, name='items_as_json'),

                       url(r'^accounts/$', views.list_inventory_accounts, name='list_inventory_accounts'),
                       url(r'^accounts/consumable/$', views.list_consumable_accounts,
                           name='list_consumable_inventory_accounts'),
                       url(r'^accounts/non-consumable/$', views.list_non_consumable_accounts,
                           name='list_non_consumable_inventory_accounts'),
                       url(r'^account/(?P<id>[0-9]+)/$', views.view_inventory_account, name='view_inventory_account'),
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
                       url(r'^demand-forms/$', views.list_demand_forms, name='list_demand_forms'),

                       url(r'^handover/incoming/$', views.handover_incoming, name='create_incoming_handover'),
                       url(r'^handover/outgoing/$', views.handover_outgoing, name='create_outgoing_handover'),
                       url(r'^save/handover/$', views.save_handover, name='save_handover'),
                       url(r'^handover/(?P<id>[0-9]+)/$', views.handover_incoming, name='update_handover'),
                       url(r'^handovers/incoming/$', views.list_incoming_handovers, name='list_incoming_handovers'),
                       url(r'^handovers/outgoing/$', views.list_outgoing_handovers, name='list_outgoing_handovers'),

                       url(r'^purchase-order/$', views.purchase_order, name='create_purchase_order'),
                       url(r'^purchase-order/(?P<id>[0-9]+)/$', views.purchase_order, name='update_purchase_order'),
                       url(r'^save/purchase_order/$', views.save_purchase_order, name='save_purchase_order'),
                       url(r'^purchase-order/(?P<id>[0-9]+)/delete$', views.delete_purchase_order,
                           name='delete_purchase_order'),
                       url(r'^purchase-orders/$', views.list_purchase_orders, name='list_purchase_orders'),

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

                       #url(r'^entry-report/$', views.entry_report, name='create_entry_report'),
                       #url(r'^purchase-order/(?P<id>[0-9]+)/$', views.purchase_order, name='update_purchase_order'),
                       #url(r'^save/purchase_order/$', views.save_purchase_order, name='save_purchase_order'),
                       #url(r'^purchase-order/(?P<id>[0-9]+)/delete$', views.delete_purchase_order,
                       #    name='delete_purchase_order'),
                       #url(r'^purchase-orders/$', views.list_purchase_orders, name='list_purchase_orders'),

)


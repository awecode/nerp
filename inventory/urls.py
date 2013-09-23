from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^items/$', views.list_inventory_items, name='list_inventory_items'),
                       url(r'^create/$', views.item_form, name='create_inventory_item'),
                       url(r'^item/delete/(?P<id>[0-9]+)$', views.delete_inventory_item, name='delete_inventory_item'),
                       url(r'^(?P<id>[0-9]+)/$', views.item_form, name='update_inventory_item'),
                       url(r'^items/json/$', views.items_as_json, name='items_as_json'),

                       url(r'^categories/$', views.list_categories, name='list_inventory_categories'),
                       url(r'^category/create/$', views.create_category, name='create_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category,
                           name='delete_inventory_category'),

                       url(r'^demand/$', views.demand_form, name='create_demand_form'),

)


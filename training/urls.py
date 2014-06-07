from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='training_index'),
                       url(r'^add/$', views.training_form, name='add_training'),
                       url(r'^(?P<pk>[0-9]+)/$', views.training_form, name='update_training'),
                       url(r'^category/add/$', views.category_form, name='add_category'),
                       url(r'^category/(?P<pk>[0-9]+)/$', views.category_form, name='update_category'),
                       url(r'^resource_person/add/$', views.resource_person_form, name='add_resource_person'),
                       url(r'^resource_person/(?P<pk>[0-9]+)/$', views.resource_person_form,
                           name='update_resource_person'),
                       url(r'^target_group/add/$', views.target_group_form, name='add_target_group'),
                       url(r'^target_group/(?P<pk>[0-9]+)/$', views.target_group_form, name='update_target_group'),
                       url(r'^participant/add/$', views.participant_form, name='add_participant'),
                       url(r'^participant/(?P<pk>[0-9]+)/$', views.participant_form, name='update_participant'),
                       url(r'^participants.json$', views.participants_as_json, name='participants_as_json'),
                       url(r'^organization/add/$', views.organization_form, name='add_organization'),
                       url(r'^organization/(?P<pk>[0-9]+)/$', views.organization_form, name='update_organization'),
                       # url(r'^author/(?P<slug>[a-zA-Z0-9_.-]+)/$', views.view_author, name='view_author'),
                       # url(r'^search/(?P<keyword>.*)$', views.search, name='search'),
)
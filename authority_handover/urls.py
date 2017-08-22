from django.conf.urls import url

from authority_handover import views

urlpatterns = [
    url(r'^$', views.AuthorityHandoverListView.as_view(), name='authority-handover-list'),
    url(r'^create/$', views.AuthorityHandoverCreate.as_view(), name='authority-handover-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.AuthorityHandoverDetailView.as_view(),
        name='authority-handover-detail'),
    # url(r'^(?P<pk>[0-9]+)/edit/$', views.AuthorityHandoverUpdateView.as_view(),
    #     name='authority-handover-edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.AuthorityHandoverDeleteView.as_view(),
        name='authority-handover-delete'),
    # url(r'^technicians/export/$', views.TechniciansExport.as_view(), name='technician-export'),
    # url(r'^technicians/import/$', views.TechniciansImport.as_view(), name='technician-import'),
]

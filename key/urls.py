from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

                       url(r'^request/$', views.send_key_request, name='send_key_request'),
                       url(r'^activation/$', views.activation, name='key_activation'),
                       # url(r'^invalid/$', views.invalid_key, name='invalid_key'),

                       )

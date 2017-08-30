# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from users import views as users_views

from authority_handover import  api as authority_handover_api

admin.autodiscover()

router = DefaultRouter()
router.register('authority-handover', authority_handover_api.AuthorityHandoverViewSet)
router.register('beneficiary', authority_handover_api.BeneficiaryViewSet)
router.register('beneficiary', authority_handover_api.BeneficiaryViewSet)


urlpatterns = [
    url(r'^$', users_views.index, name='home'),
    url(r'^user/', include('users.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^library/', include('ils.urls')),
    url(r'^training/', include('training.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^key/', include('key.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'', include('core.urls')),
    url(r'^authority-handover/', include('authority_handover.urls')),

    url(r'^api/v1/', include(router.urls)),
]

from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

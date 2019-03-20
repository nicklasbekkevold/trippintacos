from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from guest import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.guest_page, name='guest'),
    path('ajax/load-available-times/', views.load_available_times, name='ajax_load_available_times'),
    url(r'deleteme', views.deleteMe, name='deleteme'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

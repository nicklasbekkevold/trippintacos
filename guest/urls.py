from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from guest import views

urlpatterns = [
    path('', views.guest_page, name='guest'),
    path('ajax/load-available-times/', views.load_available_times, name='ajax_load_available_times'),
    path('deleteme', views.deleteMe, name='deleteme'),
    path('termsandconditions/', views.terms_and_conditions, name='terms_and_conditions')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

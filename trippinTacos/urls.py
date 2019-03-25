from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from reservations.views import cancel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='employee/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='employee/logout.html'), name='logout'),
    path('', include('guest.urls'), name='guest'),
    path('employee/', include('employee.urls'), name='employee'),
    path('reservations/', include('reservations.urls'), name='reservations'),
    path('cancel/', cancel, name='cancel'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

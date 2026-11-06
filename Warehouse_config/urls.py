from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from accounts import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('inventory/', include('inventory.urls')),
]

from django.urls import path # type: ignore
from . import views 

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('add/', views.supplier_create, name='supplier_create'),
    path('edit/<int:supplier_id>/', views.supplier_update, name='supplier_update'),
    path('delete/<int:supplier_id>/', views.supplier_delete, name='supplier_delete'),
]
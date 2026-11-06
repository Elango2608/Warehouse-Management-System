from django.urls import path  # type: ignore
from . import views

urlpatterns = [

    # Category Management
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/edit/<int:category_id>/', views.category_update, name='category_update'),
    path('categories/delete/<int:category_id>/', views.category_delete, name='category_delete'),

    # Product Management
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/edit/<int:product_id>/', views.product_update, name='product_update'),
    path('products/delete/<int:product_id>/', views.product_delete, name='product_delete'),

     # Stock URLs
    path('stock-in/', views.stock_in, name='stock_in'),
    path('stock-out/', views.stock_out, name='stock_out'),

    # Transaction History
    path('transactions/',views.transaction_history,name='transaction_history'),
]
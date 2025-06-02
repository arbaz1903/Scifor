from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Warehouse URLs
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('warehouses/new/', views.warehouse_create, name='warehouse_create'),
    path('warehouses/<int:pk>/edit/', views.warehouse_edit, name='warehouse_edit'),
    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
]
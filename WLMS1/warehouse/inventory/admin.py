from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Warehouse, Inventory, ProductCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'unit_of_measure')
    list_filter = ('category',)
    search_fields = ('name', 'sku', 'upc')

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'manager')
    search_fields = ('name', 'location')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity_on_hand', 'quantity_allocated', 'available_quantity')
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'product__sku')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
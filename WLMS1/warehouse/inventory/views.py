from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Inventory, Warehouse, ProductCategory
from .forms import ProductForm, InventoryForm, WarehouseForm, ProductCategoryForm
from .models import Warehouse
from .forms import WarehouseForm

@login_required
def dashboard(request):
    products_count = Product.objects.count()
    warehouses_count = Warehouse.objects.count()
    low_stock_count = Inventory.objects.filter(quantity_on_hand__lte=10).count()
    
    context = {
        'products_count': products_count,
        'warehouses_count': warehouses_count,
        'low_stock_count': low_stock_count,
        'title': 'Dashboard'
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    inventory = Inventory.objects.filter(product=product)
    return render(request, 'inventory/product_detail.html', {'product': product, 'inventory': inventory})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()  # SKU auto-generated here
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'inventory/product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

# Warehouse views
@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'inventory/warehouse_list.html', {'warehouses': warehouses})

@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    return render(request, 'inventory/warehouse_detail.html', {'warehouse': warehouse})

@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, 'Warehouse created successfully!')
            return redirect('warehouse_detail', pk=warehouse.pk)
    else:
        form = WarehouseForm()
    return render(request, 'inventory/warehouse_form.html', {'form': form, 'title': 'Create Warehouse'})

@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, 'Warehouse updated successfully!')
            return redirect('warehouse_detail', pk=warehouse.pk)
    else:
        form = WarehouseForm(instance=warehouse)
    return render(request, 'inventory/warehouse_form.html', {'form': form, 'warehouse': warehouse})

# Inventory views
@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    low_stock = request.GET.get('low_stock', False)
    
    if low_stock:
        inventories = inventories.filter(quantity_on_hand__lte=10)
    
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories, 'low_stock': low_stock})

@login_required
def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory updated successfully!')
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Edit Inventory'})
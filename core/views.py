from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import Product, Supplier, Order, StockAdjustment, Category
from .forms import ProductForm, SupplierForm, OrderForm, StockAdjustmentForm
from django.db import models

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {username}!')
                return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Dashboard statistics
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_orders = Order.objects.count()
    
    # Low stock products
    low_stock_products = Product.objects.filter(current_stock__lte=models.F('min_stock'))
    
    # Recent orders
    recent_orders = Order.objects.select_related('product').order_by('-order_date')[:5]
    
    # Stock value
    total_stock_value = sum(product.stock_value for product in Product.objects.all())
    
    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_orders': total_orders,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'total_stock_value': total_stock_value,
    }
    return render(request, 'dashboard.html', context)

@login_required
def product_list(request):
    products = Product.objects.select_related('category', 'supplier').all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    stock_history = StockAdjustment.objects.filter(product=product).order_by('-adjusted_at')[:10]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'stock_history': stock_history
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

@login_required
def stock_adjustment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            adjustment = form.save(commit=False)
            adjustment.product = product
            adjustment.adjusted_by = request.user
            
            if adjustment.adjustment_type == 'in':
                product.current_stock += adjustment.quantity
            elif adjustment.adjustment_type == 'out':
                product.current_stock -= adjustment.quantity
            else:  # adjustment
                product.current_stock = adjustment.quantity
            
            product.save()
            adjustment.save()
            
            messages.success(request, f'Stock adjusted successfully! New stock: {product.current_stock}')
            return redirect('product_detail', pk=product.pk)
    else:
        form = StockAdjustmentForm()
    
    return render(request, 'products/stock_adjustment.html', {
        'form': form,
        'product': product
    })

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = Product.objects.filter(supplier=supplier)
    return render(request, 'suppliers/supplier_detail.html', {
        'supplier': supplier,
        'products': products
    })

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" created successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'title': 'Add Supplier'})

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" updated successfully!')
            return redirect('supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'title': 'Edit Supplier'})

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier "{supplier_name}" deleted successfully!')
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})

@login_required
def order_list(request):
    orders = Order.objects.select_related('product').all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Order #{order.order_number} created successfully!')
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Create Order'})

@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Order #{order.order_number} updated successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Edit Order'})

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order_number = order.order_number
        order.delete()
        messages.success(request, f'Order #{order_number} deleted successfully!')
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

@login_required
def inventory_report(request):
    products = Product.objects.all()
    total_stock_value = sum(product.stock_value for product in products)
    low_stock_count = products.filter(current_stock__lte=models.F('min_stock')).count()
    out_of_stock_count = products.filter(current_stock=0).count()
    
    context = {
        'products': products,
        'total_stock_value': total_stock_value,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_products': products.count(),
    }
    return render(request, 'reports/inventory_report.html', context)
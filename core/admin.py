# from django.contrib import admin
# from .models import Supplier, Category, Product, Order, StockAdjustment, InventoryReport

# @admin.register(Supplier)
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ['name', 'contact_person', 'email', 'phone', 'created_at']
#     search_fields = ['name', 'contact_person', 'email']
#     list_filter = ['created_at']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description']
#     search_fields = ['name']

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category', 'sku', 'price', 'current_stock', 'stock_status', 'is_active']
#     list_filter = ['category', 'is_active', 'created_at']
#     search_fields = ['name', 'sku', 'description']
#     readonly_fields = ['created_at', 'updated_at']

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['order_number', 'product', 'quantity', 'customer_name', 'status', 'order_date']
#     list_filter = ['status', 'order_date']
#     search_fields = ['order_number', 'customer_name', 'customer_email']
#     readonly_fields = ['order_date']

# @admin.register(StockAdjustment)
# class StockAdjustmentAdmin(admin.ModelAdmin):
#     list_display = ['product', 'adjustment_type', 'quantity', 'reason', 'adjusted_by', 'adjusted_at']
#     list_filter = ['adjustment_type', 'adjusted_at']
#     readonly_fields = ['adjusted_at']

# @admin.register(InventoryReport)
# class InventoryReportAdmin(admin.ModelAdmin):
#     list_display = ['report_date', 'total_products', 'total_stock_value', 'low_stock_items', 'out_of_stock_items']
#     readonly_fields = ['generated_at']

from django.contrib import admin
from .models import (
    Supplier, Category, Product, PurchaseOrder, 
    PurchaseOrderItem, Order, StockAdjustment, InventoryReport
)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_at']
    search_fields = ['name', 'contact_person', 'email']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'current_stock', 'price', 'cost', 'stock_status']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['stock_status', 'stock_value']

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'status', 'total_amount', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['po_number', 'supplier__name']
    inlines = [PurchaseOrderItemInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'product', 'quantity', 'customer_name', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'customer_name', 'customer_email']

@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['product', 'adjustment_type', 'quantity', 'reason', 'adjusted_at']
    list_filter = ['adjustment_type', 'adjusted_at']
    search_fields = ['product__name', 'reason']

@admin.register(InventoryReport)
class InventoryReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'total_products', 'total_stock_value', 'generated_at']
    readonly_fields = ['generated_at']
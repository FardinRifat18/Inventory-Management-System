# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# class Supplier(models.Model):
#     name = models.CharField(max_length=200)
#     contact_person = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     address = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         ordering = ['name']

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name_plural = "Categories"

# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
#     sku = models.CharField(max_length=50, unique=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     current_stock = models.IntegerField(default=0)
#     min_stock = models.IntegerField(default=10)
#     max_stock = models.IntegerField(default=100)
#     location = models.CharField(max_length=100, blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name
    
#     @property
#     def stock_status(self):
#         if self.current_stock <= 0:
#             return 'out-of-stock'
#         elif self.current_stock <= self.min_stock:
#             return 'low-stock'
#         else:
#             return 'in-stock'
    
#     @property
#     def stock_value(self):
#         return self.current_stock * self.cost

# class Order(models.Model):
#     ORDER_STATUS = [
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled'),
#     ]
    
#     order_number = models.CharField(max_length=20, unique=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     customer_name = models.CharField(max_length=200)
#     customer_email = models.EmailField()
#     customer_phone = models.CharField(max_length=20)
#     status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
#     order_date = models.DateTimeField(auto_now_add=True)
#     expected_delivery = models.DateField(null=True, blank=True)
#     notes = models.TextField(blank=True)
    
#     def __str__(self):
#         return f"Order {self.order_number} - {self.product.name}"
    
#     @property
#     def total_amount(self):
#         return self.quantity * self.product.price

# class StockAdjustment(models.Model):
#     ADJUSTMENT_TYPES = [
#         ('in', 'Stock In'),
#         ('out', 'Stock Out'),
#         ('adjust', 'Adjustment'),
#     ]
    
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
#     quantity = models.IntegerField()
#     reason = models.CharField(max_length=200)
#     notes = models.TextField(blank=True)
#     adjusted_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     adjusted_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.adjustment_type} - {self.product.name}"

# class InventoryReport(models.Model):
#     report_date = models.DateField(default=timezone.now)
#     total_products = models.IntegerField()
#     total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)
#     low_stock_items = models.IntegerField()
#     out_of_stock_items = models.IntegerField()
#     generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     generated_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"Inventory Report - {self.report_date}"




from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=10)
    max_stock = models.IntegerField(default=100)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def stock_status(self):
        if self.current_stock <= 0:
            return 'out-of-stock'
        elif self.current_stock <= self.min_stock:
            return 'low-stock'
        else:
            return 'in-stock'
    
    @property
    def stock_value(self):
        return self.current_stock * self.cost

# Add PurchaseOrder and PurchaseOrderItem models BEFORE the Order model
class PurchaseOrder(models.Model):
    PURCHASE_ORDER_STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    po_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PURCHASE_ORDER_STATUS, default='draft')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"PO {self.po_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            # Generate PO number: PO-YYYYMMDD-001
            date_str = timezone.now().strftime('%Y%m%d')
            last_po = PurchaseOrder.objects.filter(po_number__startswith=f'PO-{date_str}').order_by('po_number').last()
            if last_po:
                last_num = int(last_po.po_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.po_number = f'PO-{date_str}-{new_num:03d}'
        super().save(*args, **kwargs)
    
    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def subtotal(self):
        return self.quantity * self.unit_cost
    
    @property
    def pending_quantity(self):
        return self.quantity - self.received_quantity

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order {self.order_number} - {self.product.name}"
    
    @property
    def total_amount(self):
        return self.quantity * self.product.price
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-001
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'ORD-{date_str}').order_by('order_number').last()
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.order_number = f'ORD-{date_str}-{new_num:03d}'
        super().save(*args, **kwargs)

class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Adjustment'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    adjusted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    adjusted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.adjustment_type} - {self.product.name}"

class InventoryReport(models.Model):
    report_date = models.DateField(default=timezone.now)
    total_products = models.IntegerField()
    total_stock_value = models.DecimalField(max_digits=15, decimal_places=2)
    low_stock_items = models.IntegerField()
    out_of_stock_items = models.IntegerField()
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inventory Report - {self.report_date}"
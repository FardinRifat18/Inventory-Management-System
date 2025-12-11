from django import forms
from .models import Product, Supplier, Order, StockAdjustment, PurchaseOrder, PurchaseOrderItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class StockAdjustmentForm(forms.Form):
    ADJUSTMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
    ]
    
    adjustment_type = forms.ChoiceField(
        choices=ADJUSTMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_delivery', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'expected_delivery': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'unit_cost']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


# from django import forms
# from .models import *
# from django.contrib.auth.models import User

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'sku': forms.TextInput(attrs={'class': 'form-control'}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'supplier': forms.Select(attrs={'class': 'form-control'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control'}),  # Changed from selling_price
#             'cost': forms.NumberInput(attrs={'class': 'form-control'}),    # Changed from cost_price
#             'current_stock': forms.NumberInput(attrs={'class': 'form-control'}),
#             'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),  # Changed from min_stock_level
#             'max_stock': forms.NumberInput(attrs={'class': 'form-control'}),  # Changed from max_stock_level
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#         }

# class StockAdjustmentForm(forms.Form):
#     ADJUSTMENT_TYPES = [
#         ('in', 'Stock In'),
#         ('out', 'Stock Out'),
#     ]
    
#     adjustment_type = forms.ChoiceField(
#         choices=ADJUSTMENT_TYPES,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     quantity = forms.IntegerField(
#         min_value=1,
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )
#     notes = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
#     )

# class PurchaseOrderForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseOrder
#         fields = ['supplier', 'expected_delivery', 'notes']
#         widgets = {
#             'supplier': forms.Select(attrs={'class': 'form-control'}),
#             'expected_delivery': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#         }

# class PurchaseOrderItemForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseOrderItem
#         fields = ['product', 'quantity', 'unit_cost']
#         widgets = {
#             'product': forms.Select(attrs={'class': 'form-control'}),
#             'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
#             'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#         }

# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = '__all__'
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#         }
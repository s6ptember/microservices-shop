from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal', 'created_at', 'updated_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'total_items', 'total_amount', 'created_at']
    inlines = [CartItemInline]
    readonly_fields = ['total_amount', 'total_items', 'created_at', 'updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product_id', 'product_name',
        'quantity', 'price', 'subtotal']
    list_filter = ['created_at']
    readonly_fields = ['subtotal', 'created_at', 'updated_at']

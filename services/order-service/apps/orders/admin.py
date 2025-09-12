from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_id', 'user_name', 'status', 'total_amount',
        'items_count', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user_email', 'user_name']
    inlines = [OrderItemInline]
    readonly_fields = ['total_quantity', 'items_count', 'created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related().prefetch_related('items')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order', 'product_name', 'quantity', 'price', 'subtotal'
    ]
    list_filter = ['created_at']
    readonly_fields = ['subtotal', 'created_at']

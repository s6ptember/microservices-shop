# ===== services/product-service/apps/products/admin.py =====
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'products_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def products_count(self, obj):
        count = obj.products.count()
        url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} products</a>', url, count)
    products_count.short_description = 'Products Count'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview', 'name', 'category', 'price', 'stock_quantity',
        'is_active', 'is_in_stock', 'created_at'
    ]
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock_quantity', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'image_preview_large']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity'),
            'classes': ('collapse',)
        }),
        ('Image', {
            'fields': ('image_url', 'image_preview_large'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image_url
            )
        return "No Image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image_url
            )
        return "No Image"
    image_preview_large.short_description = 'Image Preview'

    def is_in_stock(self, obj):
        if obj.stock_quantity > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ In Stock ({})</span>',
                obj.stock_quantity
            )
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Out of Stock</span>')
    is_in_stock.short_description = 'Stock Status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

    # Действия для массового управления
    actions = ['make_active', 'make_inactive', 'duplicate_products']

    def make_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} products were successfully activated.')
    make_active.short_description = "Activate selected products"

    def make_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} products were successfully deactivated.')
    make_inactive.short_description = "Deactivate selected products"

    def duplicate_products(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.name = f"Copy of {product.name}"
            product.save()
        count = queryset.count()
        self.message_user(request, f'{count} products were successfully duplicated.')
    duplicate_products.short_description = "Duplicate selected products"

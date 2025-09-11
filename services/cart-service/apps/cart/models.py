from django.db import models
from decimal import Decimal

class Cart(models.Model):
    user_id = models.IntegerField(unique=True)  # ID пользователя из user-service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for user {self.user_id}"

    @property
    def total_amount(self):
        """Общая сумма корзины"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Общее количество товаров"""
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        """Очистка корзины"""
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()  # ID товара из product-service
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент добавления
    product_name = models.CharField(max_length=200, blank=True)  # Кэш названия
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product_id']

    def __str__(self):
        return f"{self.quantity}x {self.product_name or f'Product {self.product_id}'}"

    @property
    def subtotal(self):
        """Подсумма для данного товара"""
        return self.price * self.quantity

from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_id', 'product_name', 'quantity',
            'price', 'subtotal', 'created_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user_id', 'status', 'total_amount', 'shipping_address',
            'user_email', 'user_name', 'items', 'items_count', 'total_quantity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'total_amount', 'user_email', 'user_name']

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(max_length=500)

    def validate_shipping_address(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Shipping address is too short")
        return value.strip()

class UpdateOrderStatusSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES)

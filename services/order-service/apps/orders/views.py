from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, CreateOrderSerializer,
    UpdateOrderStatusSerializer
)
from .services import CartService, ProductService, UserService, event_bus
import logging

logger = logging.getLogger(__name__)

class IsAuthenticatedCustom:
    """Custom permission class that checks if user_id is set by middleware"""

    def has_permission(self, request, view):
        return hasattr(request, 'user_id') and request.user_id is not None

class OrderListView(generics.ListAPIView):
    """Список заказов пользователя"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user_id)


class OrderDetailView(generics.RetrieveAPIView):
    """Детали заказа"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs['pk'], user_id=self.request.user_id)

@api_view(['POST'])
@permission_classes([IsAuthenticatedCustom])
def create_order(request):
    """Создание заказа из корзины"""
    logger.info(f"Creating order for user {request.user_id} with data: {request.data}")

    # Извлекаем данные из запроса
    shipping_address = request.data.get('shipping_address', '')
    customer_info = request.data.get('customer_info', {})
    special_instructions = request.data.get('special_instructions', '')

    if not shipping_address:
        return Response({
            'error': 'Shipping address is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id

    try:
        with transaction.atomic():
            # Получаем корзину пользователя
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            cart_data = CartService.get_user_cart(user_id, token)

            if not cart_data or not cart_data.get('items'):
                return Response({
                    'error': 'Cart is empty'
                }, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Cart data for user {user_id}: {len(cart_data['items'])} items")

            # Получаем информацию о пользователе
            user_data = UserService.get_user_from_token(token)
            if not user_data:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Подготавливаем данные для резервирования
            items_to_reserve = []
            for cart_item in cart_data['items']:
                items_to_reserve.append({
                    'product_id': cart_item['product_id'],
                    'quantity': cart_item['quantity']
                })

            # Резервируем товары
            logger.info(f"Reserving products: {items_to_reserve}")
            if not ProductService.reserve_products(items_to_reserve):
                return Response({
                    'error': 'Failed to reserve products. Some items may be out of stock.'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Формируем имя пользователя
                user_name = ''
                if customer_info:
                    user_name = f"{customer_info.get('first_name', '')} {customer_info.get('last_name', '')}".strip()

                if not user_name:
                    user_name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()

                # Создаем заказ
                order = Order.objects.create(
                    user_id=user_id,
                    shipping_address=shipping_address,
                    user_email=customer_info.get('email') or user_data.get('email', ''),
                    user_name=user_name,
                    total_amount=cart_data['total_amount']
                )

                logger.info(f"Created order {order.id} for user {user_id}")

                # Создаем позиции заказа
                order_items = []
                for cart_item in cart_data['items']:
                    order_item = OrderItem.objects.create(
                        order=order,
                        product_id=cart_item['product_id'],
                        product_name=cart_item['product_name'],
                        quantity=cart_item['quantity'],
                        price=cart_item['price']
                    )
                    order_items.append({
                        'product_id': order_item.product_id,
                        'quantity': order_item.quantity,
                        'product_name': order_item.product_name,
                        'price': str(order_item.price)
                    })

                # Добавляем специальные инструкции как комментарий
                if special_instructions:
                    order.shipping_address += f"\n\nSpecial Instructions: {special_instructions}"
                    order.save()

                # Публикуем событие о создании заказа
                event_bus.publish_event('order.created', {
                    'order_id': order.id,
                    'user_id': order.user_id,
                    'total_amount': str(order.total_amount),
                    'items': order_items,
                    'customer_info': customer_info
                })

                logger.info(f"Order {order.id} created successfully for user {user_id}")

                return Response(
                    OrderSerializer(order).data,
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                # Если создание заказа не удалось, освобождаем товары
                logger.error(f"Failed to create order, releasing products: {e}")
                ProductService.release_products(items_to_reserve)
                raise

    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return Response({
            'error': 'Failed to create order',
            'details': str(e) if request.user_id else 'Please try again'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticatedCustom])
def update_order_status(request, pk):
    """Обновление статуса заказа (только для администраторов)"""
    order = get_object_or_404(Order, id=pk)

    serializer = UpdateOrderStatusSerializer(data=request.data)
    if serializer.is_valid():
        old_status = order.status
        new_status = serializer.validated_data['status']

        # Проверяем валидность перехода статуса
        if not is_valid_status_transition(old_status, new_status):
            return Response({
                'error': f'Invalid status transition from {old_status} to {new_status}'
            }, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()

        # Публикуем событие об изменении статуса
        event_bus.publish_event('order.status_changed', {
            'order_id': order.id,
            'user_id': order.user_id,
            'old_status': old_status,
            'new_status': new_status
        })

        # Если заказ отменен, освобождаем товары
        if new_status == 'cancelled':
            items_to_release = []
            for item in order.items.all():
                items_to_release.append({
                    'product_id': item.product_id,
                    'quantity': item.quantity
                })
            ProductService.release_products(items_to_release)

            event_bus.publish_event('order.cancelled', {
                'order_id': order.id,
                'user_id': order.user_id,
                'items': items_to_release
            })

        return Response(OrderSerializer(order).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def is_valid_status_transition(old_status: str, new_status: str) -> bool:
    """Проверка валидности перехода между статусами"""
    valid_transitions = {
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['shipped', 'cancelled'],
        'shipped': ['delivered', 'cancelled'],
        'delivered': [],  # Финальный статус
        'cancelled': []   # Финальный статус
    }

    return new_status in valid_transitions.get(old_status, [])

@api_view(['GET'])
@permission_classes([IsAuthenticatedCustom])
def order_statistics(request):
    """Статистика заказов пользователя"""
    user_id = request.user_id
    orders = Order.objects.filter(user_id=user_id)

    stats = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'confirmed_orders': orders.filter(status='confirmed').count(),
        'shipped_orders': orders.filter(status='shipped').count(),
        'delivered_orders': orders.filter(status='delivered').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
        'total_spent': sum(order.total_amount for order in orders if order.status != 'cancelled')
    }

    return Response(stats)

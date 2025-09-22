from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from unittest.mock import patch, MagicMock
from .models import Order, OrderItem
from .services import CartService, ProductService, UserService


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            user_id=1,
            status='pending',
            total_amount=Decimal('199.98'),
            shipping_address='123 Test St, Test City',
            user_email='test@example.com',
            user_name='John Doe'
        )

    def test_order_creation(self):
        """Test order creation"""
        self.assertEqual(self.order.user_id, 1)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.total_amount, Decimal('199.98'))
        self.assertEqual(str(self.order), "Order #1 by User 1")

    def test_order_items_count(self):
        """Test items count property"""
        # Initially no items
        self.assertEqual(self.order.items_count, 0)

        # Add some items
        OrderItem.objects.create(
            order=self.order,
            product_id=1,
            product_name='Test Product',
            quantity=2,
            price=Decimal('50.00')
        )
        OrderItem.objects.create(
            order=self.order,
            product_id=2,
            product_name='Another Product',
            quantity=1,
            price=Decimal('99.98')
        )

        self.assertEqual(self.order.items_count, 2)

    def test_total_quantity(self):
        """Test total quantity property"""
        OrderItem.objects.create(
            order=self.order,
            product_id=1,
            product_name='Test Product',
            quantity=2,
            price=Decimal('50.00')
        )
        OrderItem.objects.create(
            order=self.order,
            product_id=2,
            product_name='Another Product',
            quantity=3,
            price=Decimal('33.32')
        )

        self.assertEqual(self.order.total_quantity, 5)

    def test_calculate_total(self):
        """Test calculate total method"""
        OrderItem.objects.create(
            order=self.order,
            product_id=1,
            product_name='Test Product',
            quantity=2,
            price=Decimal('50.00')
        )
        OrderItem.objects.create(
            order=self.order,
            product_id=2,
            product_name='Another Product',
            quantity=1,
            price=Decimal('99.98')
        )

        total = self.order.calculate_total()
        expected_total = Decimal('199.98')  # 2*50 + 1*99.98
        self.assertEqual(total, expected_total)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            user_id=1,
            status='pending',
            total_amount=Decimal('100.00'),
            shipping_address='123 Test St',
            user_email='test@example.com'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product_id=1,
            product_name='Test Product',
            quantity=2,
            price=Decimal('50.00')
        )

    def test_order_item_creation(self):
        """Test order item creation"""
        self.assertEqual(self.order_item.product_id, 1)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, Decimal('50.00'))
        self.assertEqual(str(self.order_item), '2x Test Product')

    def test_subtotal_property(self):
        """Test subtotal calculation"""
        expected_subtotal = Decimal('100.00')  # 2 * 50.00
        self.assertEqual(self.order_item.subtotal, expected_subtotal)


class OrderAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_id = 1

        # Mock user authentication
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer fake-jwt-token'

        self.order = Order.objects.create(
            user_id=self.user_id,
            status='pending',
            total_amount=Decimal('199.98'),
            shipping_address='123 Test St',
            user_email='test@example.com',
            user_name='John Doe'
        )

    def test_get_orders_list_unauthenticated(self):
        """Test getting orders without authentication"""
        client = APIClient()  # New client without auth
        url = reverse('order-list')
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('apps.orders.middleware.UserService.get_user_from_token')
    def test_get_orders_list_authenticated(self, mock_get_user):
        """Test getting orders with authentication"""
        mock_get_user.return_value = {
            'id': self.user_id,
            'email': 'test@example.com'
        }

        # Mock the middleware by setting user_id
        def mock_middleware(request):
            request.user_id = self.user_id
            return request

        with patch('apps.orders.views.OrderListView.get_queryset') as mock_queryset:
            mock_queryset.return_value = Order.objects.filter(user_id=self.user_id)

            url = reverse('order-list')
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('apps.orders.services.CartService.get_user_cart')
    @patch('apps.orders.services.ProductService.reserve_products')
    @patch('apps.orders.services.UserService.get_user_from_token')
    def test_create_order_success(self, mock_get_user, mock_reserve, mock_get_cart):
        """Test successful order creation"""
        # Mock service responses
        mock_get_user.return_value = {
            'id': self.user_id,
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        mock_get_cart.return_value = {
            'items': [
                {
                    'product_id': 1,
                    'product_name': 'Test Product',
                    'quantity': 2,
                    'price': Decimal('50.00')
                }
            ],
            'total_amount': Decimal('100.00')
        }

        mock_reserve.return_value = True

        # Mock the middleware
        def add_user_id(request):
            request.user_id = self.user_id
            return None

        with patch('apps.orders.middleware.JWTAuthenticationMiddleware.__call__', side_effect=add_user_id):
            url = reverse('create-order')
            data = {
                'shipping_address': '456 New Address St, New City',
                'customer_info': {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john@example.com'
                }
            }

            response = self.client.post(url, data, format='json')

            # Should create order successfully
            self.assertTrue(Order.objects.filter(user_id=self.user_id).exists())

    def test_create_order_no_shipping_address(self):
        """Test order creation without shipping address"""
        url = reverse('create-order')
        data = {}

        # Mock middleware
        def add_user_id(request):
            request.user_id = self.user_id
            return None

        with patch('apps.orders.middleware.JWTAuthenticationMiddleware.__call__', side_effect=add_user_id):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_statistics(self):
        """Test getting order statistics"""
        # Create orders with different statuses
        Order.objects.create(
            user_id=self.user_id,
            status='confirmed',
            total_amount=Decimal('50.00'),
            shipping_address='Address 1'
        )
        Order.objects.create(
            user_id=self.user_id,
            status='delivered',
            total_amount=Decimal('75.00'),
            shipping_address='Address 2'
        )

        # Mock middleware
        def add_user_id(request):
            request.user_id = self.user_id
            return None

        with patch('apps.orders.middleware.JWTAuthenticationMiddleware.__call__', side_effect=add_user_id):
            url = reverse('order-statistics')
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['total_orders'], 3)  # Including setUp order
            self.assertEqual(response.data['confirmed_orders'], 1)
            self.assertEqual(response.data['delivered_orders'], 1)


class ServiceTest(TestCase):
    """Test external service integrations"""

    @patch('requests.get')
    def test_cart_service_get_user_cart(self, mock_get):
        """Test CartService.get_user_cart method"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [{'product_id': 1, 'quantity': 2}],
            'total_amount': '100.00'
        }
        mock_get.return_value = mock_response

        result = CartService.get_user_cart(1, 'fake-token')

        self.assertIsNotNone(result)
        self.assertEqual(len(result['items']), 1)

    @patch('requests.get')
    def test_cart_service_failure(self, mock_get):
        """Test CartService when service is down"""
        mock_get.side_effect = Exception('Service unavailable')

        result = CartService.get_user_cart(1, 'fake-token')

        self.assertIsNone(result)

    @patch('requests.post')
    def test_product_service_reserve_products(self, mock_post):
        """Test ProductService.reserve_products method"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        items = [{'product_id': 1, 'quantity': 2}]
        result = ProductService.reserve_products(items)

        self.assertTrue(result)
        mock_post.assert_called()

    @patch('requests.get')
    def test_user_service_get_user_from_token(self, mock_get):
        """Test UserService.get_user_from_token method"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'email': 'test@example.com',
            'first_name': 'John'
        }
        mock_get.return_value = mock_response

        result = UserService.get_user_from_token('fake-token')

        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 1)


class OrderStatusTransitionTest(TestCase):
    """Test order status transitions"""

    def setUp(self):
        self.order = Order.objects.create(
            user_id=1,
            status='pending',
            total_amount=Decimal('100.00'),
            shipping_address='123 Test St'
        )

    def test_valid_status_transitions(self):
        """Test valid status transitions"""
        from apps.orders.views import is_valid_status_transition

        # Valid transitions
        self.assertTrue(is_valid_status_transition('pending', 'confirmed'))
        self.assertTrue(is_valid_status_transition('confirmed', 'shipped'))
        self.assertTrue(is_valid_status_transition('shipped', 'delivered'))

        # Invalid transitions
        self.assertFalse(is_valid_status_transition('delivered', 'shipped'))
        self.assertFalse(is_valid_status_transition('cancelled', 'confirmed'))

    @patch('apps.orders.services.ProductService.release_products')
    def test_order_cancellation_releases_products(self, mock_release):
        """Test that cancelling order releases products"""
        OrderItem.objects.create(
            order=self.order,
            product_id=1,
            product_name='Test Product',
            quantity=2,
            price=Decimal('50.00')
        )

        # Mock middleware to add user_id
        def add_user_id(request):
            request.user_id = 1
            return None

        with patch('apps.orders.middleware.JWTAuthenticationMiddleware.__call__', side_effect=add_user_id):
            client = APIClient()
            client.defaults['HTTP_AUTHORIZATION'] = 'Bearer fake-token'

            url = reverse('update-order-status', kwargs={'pk': self.order.pk})
            data = {'status': 'cancelled'}

            response = client.put(url, data, format='json')

            # Should call release_products
            mock_release.assert_called_once()

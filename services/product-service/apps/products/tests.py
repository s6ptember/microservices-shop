from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )

    def test_category_creation(self):
        """Test category creation and slug generation"""
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.slug, 'electronics')
        self.assertEqual(str(self.category), 'Electronics')

    def test_category_slug_generation(self):
        """Test automatic slug generation"""
        category = Category.objects.create(name='Home & Garden')
        self.assertEqual(category.slug, 'home-garden')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='iPhone 15',
            description='Latest iPhone',
            price=Decimal('999.99'),
            category=self.category,
            stock_quantity=50
        )

    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, 'iPhone 15')
        self.assertEqual(self.product.price, Decimal('999.99'))
        self.assertEqual(self.product.category, self.category)
        self.assertTrue(self.product.is_in_stock)
        self.assertTrue(self.product.is_active)

    def test_product_string_representation(self):
        """Test product string representation"""
        self.assertEqual(str(self.product), 'iPhone 15')

    def test_is_in_stock_property(self):
        """Test is_in_stock property"""
        self.assertTrue(self.product.is_in_stock)

        self.product.stock_quantity = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)

    def test_reserve_quantity_success(self):
        """Test successful quantity reservation"""
        initial_stock = self.product.stock_quantity
        result = self.product.reserve_quantity(5)

        self.assertTrue(result)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, initial_stock - 5)

    def test_reserve_quantity_insufficient_stock(self):
        """Test reservation with insufficient stock"""
        result = self.product.reserve_quantity(100)

        self.assertFalse(result)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 50)  # Unchanged

    def test_release_quantity(self):
        """Test releasing reserved quantity"""
        initial_stock = self.product.stock_quantity
        self.product.release_quantity(10)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, initial_stock + 10)


class ProductAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='iPhone 15',
            description='Latest iPhone',
            price=Decimal('999.99'),
            category=self.category,
            stock_quantity=50
        )

    def test_get_products_list(self):
        """Test getting products list"""
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_product_detail(self):
        """Test getting product detail"""
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'iPhone 15')

    def test_filter_products_by_price(self):
        """Test filtering products by price range"""
        url = reverse('product-list')
        response = self.client.get(url, {'min_price': 500, 'max_price': 1500})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_products_in_stock(self):
        """Test filtering products in stock"""
        # Create out of stock product
        Product.objects.create(
            name='Out of Stock Item',
            description='No stock',
            price=Decimal('50.00'),
            category=self.category,
            stock_quantity=0
        )

        url = reverse('product-list')
        response = self.client.get(url, {'in_stock': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_reserve_product_success(self):
        """Test successful product reservation"""
        url = reverse('reserve-product', kwargs={'product_id': self.product.pk})
        data = {'quantity': 5}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['remaining_stock'], 45)

    def test_reserve_product_insufficient_stock(self):
        """Test product reservation with insufficient stock"""
        url = reverse('reserve-product', kwargs={'product_id': self.product.pk})
        data = {'quantity': 100}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_release_product(self):
        """Test releasing reserved product"""
        # First reserve some quantity
        self.product.reserve_quantity(10)

        url = reverse('release-product', kwargs={'product_id': self.product.pk})
        data = {'quantity': 5}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_check_availability(self):
        """Test checking product availability"""
        url = reverse('check-availability', kwargs={'product_id': self.product.pk})
        response = self.client.get(url, {'quantity': 10})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])
        self.assertEqual(response.data['stock_quantity'], 50)


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )

    def test_get_categories_list(self):
        """Test getting categories list"""
        url = reverse('category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_category_detail(self):
        """Test getting category detail"""
        url = reverse('category-detail', kwargs={'slug': self.category.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')
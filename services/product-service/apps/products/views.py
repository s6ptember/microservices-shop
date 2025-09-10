from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product
from .serializers import (
    CategorySerializer, ProductSerializer,
    ProductDetailSerializer, ProductCreateUpdateSerializer
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтр по цене
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Фильтр по наличию
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

@api_view(['POST'])
def reserve_product(request, product_id):
    """Резервирование товара для заказа"""
    try:
        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity', 1)

        if product.reserve_quantity(quantity):
            return Response({
                'success': True,
                'message': f'Reserved {quantity} units of {product.name}',
                'remaining_stock': product.stock_quantity
            })
        else:
            return Response({
                'success': False,
                'message': 'Insufficient stock',
                'available_stock': product.stock_quantity
            }, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def release_product(request, product_id):
    """Освобождение зарезервированного товара"""
    try:
        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity', 1)

        product.release_quantity(quantity)
        return Response({
            'success': True,
            'message': f'Released {quantity} units of {product.name}',
            'current_stock': product.stock_quantity
        })

    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def check_availability(request, product_id):
    """Проверка наличия товара"""
    try:
        product = Product.objects.get(id=product_id)
        quantity = int(request.query_params.get('quantity', 1))

        return Response({
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'available': product.stock_quantity >= quantity,
            'stock_quantity': product.stock_quantity,
            'requested_quantity': quantity
        })

    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)

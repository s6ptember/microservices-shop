from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reserve/', views.reserve_product, name='reserve-product'),
    path('products/<int:product_id>/release/', views.release_product, name='release-product'),
    path('products/<int:product_id>/check-availability/', views.check_availability, name='check-availability'),
]

from django.urls import re_path
from . import views

# Все API запросы проксируем к соответствующим сервисам
urlpatterns = [
    # User service routes
    re_path(r'^auth/.*', views.proxy_view, name='auth-proxy'),
    re_path(r'^users/.*', views.proxy_view, name='users-proxy'),

    # Product service routes
    re_path(r'^products/.*', views.proxy_view, name='products-proxy'),
    re_path(r'^categories/.*', views.proxy_view, name='categories-proxy'),

    # Cart service routes
    re_path(r'^cart/.*', views.proxy_view, name='cart-proxy'),

    # Order service routes
    re_path(r'^orders/.*', views.proxy_view, name='orders-proxy'),
]

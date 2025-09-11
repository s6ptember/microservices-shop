from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart-detail'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove-cart-item'),
    path('cart/clear/', views.clear_cart, name='clear-cart'),
    path('cart/summary/', views.cart_summary, name='cart-summary'),
]

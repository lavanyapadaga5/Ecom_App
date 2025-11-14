from django.urls import path
from .views import (
    OrderCreateView, OrderListView,
    CartView, AddToCartView,
    UpdateCartItemView, RemoveCartItemView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]

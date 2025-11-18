from django.urls import path
from .views import (
    OrderCreateView, OrderListView,
    CartView, BulkAddToCartView,
    UpdateCartItemView, RemoveCartItemView, OrderHistoryView, PlaceOrderView, CancelOrderView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', BulkAddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path("orders/history/", OrderHistoryView.as_view(), name="order-history"),
    path("place-order/", PlaceOrderView.as_view(), name="place_order"),
    path("cancel-order/<int:order_id>/", CancelOrderView.as_view(), name="cancel_order"),
]

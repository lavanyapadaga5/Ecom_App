from django.urls import path
from .views import ProductListCreateView, ProductDetailView, AddToWishlistView, RemoveFromWishlistView, WishlistView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('wishlist/add/', AddToWishlistView.as_view(), name='wishlist-add'),
    path('wishlist/remove/', RemoveFromWishlistView.as_view(), name='wishlist-remove'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
]

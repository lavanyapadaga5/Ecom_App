from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Wishlist, Product
from .serializers import WishlistSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AddToWishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if already in wishlist
        exists = Wishlist.objects.filter(user=request.user, product=product).exists()

        if exists:
            return Response({"message": "Already in wishlist"}, status=status.HTTP_200_OK)

        Wishlist.objects.create(user=request.user, product=product)

        return Response({"message": "Added to wishlist"}, status=status.HTTP_201_CREATED)

class RemoveFromWishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        product_id = request.data.get("product_id")
        user = request.user

        try:
            wishlist_item = Wishlist.objects.get(user=user, product_id=product_id)
            wishlist_item.delete()
            return Response({"message": "Removed from wishlist"}, status=200)
        except Wishlist.DoesNotExist:
            return Response({"error": "Item not in wishlist"}, status=404)


class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        items = Wishlist.objects.filter(user=user)
        serializer = WishlistSerializer(items, many=True)
        return Response(serializer.data, status=200)
















































































































































































































































































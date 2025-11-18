from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer
)
from products.models import Product
from billing.serializers import ProductSerializer


# -------------------- ORDER CREATE --------------------
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        serializer = super().get_serializer(*args, **kwargs)

        for field in getattr(serializer, 'fields', {}).values():
            try:
                if getattr(field, 'child', None):
                    nested = field.child
                    if hasattr(nested, 'fields') and 'product' in nested.fields:
                        nested.fields['product'].queryset = Product.objects.all()
                else:
                    if hasattr(field, 'fields') and 'product' in field.fields:
                        field.fields['product'].queryset = Product.objects.all()
            except Exception:
                pass
        return serializer


# -------------------- ORDER LIST --------------------
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# -------------------- VIEW CART --------------------
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


# -------------------- ADD TO CART --------------------

class BulkAddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        items = request.data.get("items", [])
        if not items:
            return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user)
        added_items = []

        for item in items:
            product_id = item.get("product_id")
            quantity = int(item.get("quantity", 1))

            product = get_object_or_404(Product, id=product_id)

            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product
            )

            if not item_created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()
            added_items.append(cart_item)

        serializer = CartItemSerializer(added_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED) """
 
class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not quantity:
            return Response({'error': 'quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user's cart
        cart = get_object_or_404(Cart, user=request.user)

        # Find the CartItem by product_id
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        # Update quantity
        cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response({
            "message": "Item updated successfully",
            "item": serializer.data
        }, status=status.HTTP_200_OK)


# -------------------- UPDATE CART ITEM --------------------
"""class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):  # pk matches your URL pattern
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)

        quantity = request.data.get('quantity')
        if not quantity:
            return Response({'error': 'Quantity required'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK) """


# -------------------- REMOVE CART ITEM --------------------
class RemoveCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        # Get the user's cart
        cart = get_object_or_404(Cart, user=request.user)

        # Try to get the cart item for this product
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"error": "No CartItem matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the cart item
        cart_item.delete()

        # Return success response
        return Response({"message": "Item removed from cart successfully."}, status=status.HTTP_200_OK)
        
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get user's cart
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"error": "No cart found"}, status=400)

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "Your cart is empty"}, status=400)

        # Create order
        order = Order.objects.create(
            user=request.user,
            total=0
        )

        total_price = 0

        # Move cart items to order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_price += item.product.price * item.quantity

        # Update order total
        order.total = total_price
        order.save()

        # Clear cart
        cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total": order.total
        }, status=201)
    
class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        # get user order
        order = Order.objects.filter(id=order_id, user=request.user).first()

        if not order:
            return Response({"error": "Order not found"}, status=404)

        if order.status == "cancelled":
            return Response({"message": "Order is already cancelled"}, status=400)

        # cancel the order
        order.status = "cancelled"
        order.save()

        return Response({
            "message": "Order cancelled successfully",
            "order_id": order.id
        }, status=200)


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-placed_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
        
   

    
    
    
    
    

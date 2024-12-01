from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Product, FarmerProduct, Order, OrderItem, Cart, CartItem
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    FarmerProductSerializer,
    FarmerProductCreateUpdateSerializer,
    OrderSerializer
)
from .permissions import IsBuyerOrReadOnly, IsFarmer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

class ProductCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # Check if the input is a list
        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of products"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FarmerProductListView(generics.ListAPIView):
    serializer_class = FarmerProductSerializer
    permission_classes = [IsAuthenticated, IsFarmer] 

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)

class FarmerProductCreateView(generics.CreateAPIView):
    serializer_class = FarmerProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsFarmer]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

class FarmerProductUpdateView(generics.UpdateAPIView):
    serializer_class = FarmerProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsFarmer]

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)

class FarmerProductDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsFarmer] 

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)

class ProductNamesByCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category):
        valid_names = Product.PRODUCT_NAME_CHOICES.get(category, [])
        if not valid_names:
            return Response({"error": f"No valid product names found for category '{category}'."}, status=400)
        return Response({"category": category, "valid_names": valid_names})

class OrderListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        farmer_product_id = request.data.get('farmer_product_id')
        quantity = request.data.get('quantity', 1)

        # Get or create the cart
        cart, created = Cart.objects.get_or_create(user=user)

        # Get the FarmerProduct
        try:
            farmer_product = FarmerProduct.objects.get(id=farmer_product_id)
        except FarmerProduct.DoesNotExist:
            return Response({"error": "FarmerProduct not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check stock
        if farmer_product.available_quantity < quantity:
            return Response(
                {"error": f"Only {farmer_product.available_quantity} items available."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, farmer_product=farmer_product)
        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Product added to cart."}, status=status.HTTP_200_OK)

class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty."}, status=status.HTTP_404_NOT_FOUND)

        items = [
            {
                "farmer_product_id": item.farmer_product.id,
                "product_name": item.farmer_product.product.name,
                "quantity": item.quantity,
                "price": str(item.farmer_product.price),
                "total_price": str(item.quantity * item.farmer_product.price),
            }
            for item in cart.items.all()
        ]

        total_cart_price = sum(item["total_price"] for item in items)

        return Response({"items": items, "total_cart_price": str(total_cart_price)}, status=status.HTTP_200_OK)
    
class CheckoutCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty."}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({"error": "Cart has no items."}, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        order = Order.objects.create(user=user)
        for item in cart.items.all():
            # Reduce FarmerProduct stock
            if item.quantity > item.farmer_product.available_quantity:
                return Response(
                    {"error": f"Insufficient stock for {item.farmer_product.product.name}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.farmer_product.available_quantity -= item.quantity
            item.farmer_product.save()

            # Add to OrderItem
            OrderItem.objects.create(
                order=order,
                product=item.farmer_product.product,
                quantity=item.quantity,
                price=item.farmer_product.price
            )

        # Clear the cart
        cart.items.all().delete()

        return Response({"message": "Order placed successfully.", "order_id": order.id}, status=status.HTTP_201_CREATED)

class CartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, farmer_product_id):
        try:
            cart_item = CartItem.objects.get(user=request.user, farmer_product_id=farmer_product_id)
            cart_item.delete()
            return Response({"detail": "Product removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
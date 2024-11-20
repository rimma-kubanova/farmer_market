from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Product, FarmerProduct
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    FarmerProductSerializer,
    FarmerProductCreateUpdateSerializer,
)
from .permissions import IsBuyerOrReadOnly, IsFarmer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]


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

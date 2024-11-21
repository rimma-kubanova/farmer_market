from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
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
    permission_classes = [AllowAny]

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)

class FarmerProductCreateView(generics.CreateAPIView):
    serializer_class = FarmerProductCreateUpdateSerializer
    permission_classes = [AllowAny] 

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

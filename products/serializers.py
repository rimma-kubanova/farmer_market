from rest_framework import serializers
from .models import Product, FarmerProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class FarmerProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.username', read_only=True)

    class Meta:
        model = FarmerProduct
        fields = ['id', 'farmer_name', 'product', 'available_quantity', 'price']

class ProductDetailSerializer(serializers.ModelSerializer):
    farmer_products = FarmerProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at', 'farmer_products']

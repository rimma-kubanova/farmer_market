from rest_framework import serializers
from .models import Product, FarmerProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        category = data.get('category')
        name = data.get('name')

        # Get valid names for the chosen category
        valid_names = Product.PRODUCT_NAME_CHOICES.get(category, [])

        if name not in valid_names:
            raise serializers.ValidationError(
                f"Invalid product name '{name}' for category '{category}'. Valid options are: {', '.join(valid_names)}"
            )
        return data


class FarmerProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.username', read_only=True)

    class Meta:
        model = FarmerProduct
        fields = ['id', 'farmer_name', 'product', 'available_quantity', 'price']

class ProductDetailSerializer(serializers.ModelSerializer):
    farmer_products = FarmerProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created_at', 'updated_at', 'farmer_products']

class FarmerProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProduct
        fields = ['id', 'product', 'available_quantity', 'price']
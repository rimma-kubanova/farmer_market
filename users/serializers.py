from rest_framework import serializers
from .models import CustomUser, BuyerProfile, FarmerProfile

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['preferred_categories']

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['farm_size']

class UserSerializer(serializers.ModelSerializer):
    buyer_profile = BuyerSerializer(required=False)
    farmer_profile = FarmerSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'buyer_profile', 'farmer_profile', 'address']

    def create(self, validated_data):
        user_type = validated_data.get('user_type')
        buyer_data = validated_data.pop('buyer_profile', None)
        farmer_data = validated_data.pop('farmer_profile', None)

        user = CustomUser.objects.create(**validated_data)

        if user_type == 'buyer' and buyer_data:
            BuyerProfile.objects.create(user=user, **buyer_data)
        elif user_type == 'farmer' and farmer_data:
            FarmerProfile.objects.create(user=user, **farmer_data)
        return user

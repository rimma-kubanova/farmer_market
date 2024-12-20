from rest_framework import serializers
from .models import User, BuyerProfile, FarmerProfile
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')
        user = authenticate(username=username_or_email, password=password)

        if not user:
            user = User.objects.filter(email=username_or_email).first()
            if user and user.check_password(password):
                return user
            raise serializers.ValidationError("Invalid credentials")
        return user

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['delivery_address']

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['document_id', 'farm_size', 'farm_location']

class UserSerializer(serializers.ModelSerializer):
    buyer_profile = BuyerProfileSerializer(read_only=True)
    farmer_profile = FarmerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'buyer_profile', 'farmer_profile']
        read_only_fields = ['id']
        
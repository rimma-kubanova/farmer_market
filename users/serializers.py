from rest_framework import serializers
from .models import User
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

from .models import User, FarmerProfile
from .serializers import RegisterSerializer, LoginSerializer, BuyerProfileSerializer, FarmerProfileSerializer, UserSerializer
from django.contrib.auth import authenticate, login
from users.utils import notify_farmer_approval
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

class RegisterView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, role):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            if user.is_superuser:
                return Response(
                    {"token": token.key, "role": user.role, "message": "Superuser logged in successfully"},
                    status=status.HTTP_200_OK
                )
            return Response({"token": token.key, "role": user.role}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})

class UpdateBuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = request.user.buyer_profile
        serializer = BuyerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)

class UpdateFarmerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile = request.user.farmer_profile
        serializer = FarmerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        # Allow admin users to perform all actions; non-admins can only view users
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get the current logged-in user's details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_queryset(self):
        # Optionally filter by role if a query parameter is provided
        role = self.request.query_params.get('role')
        if role:
            return self.queryset.filter(role=role)
        return super().get_queryset()
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register_superuser(self, request):
        """Create a new superuser."""
        data = request.data
        password = data.get("password")

        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_superuser(
                username=data.get("username"),
                email=data.get("email"),
                password=password
            )
            return Response({"message": f"Superuser '{user.username}' created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ApproveFarmerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, farmer_id):
        try:
            user = User.objects.get(id=farmer_id)
            if user.role != 'farmer':
                return Response({'error': 'User is not a farmer.'}, status=400)

            farmer_profile = user.farmer_profile
            farmer_profile.is_approved = True
            farmer_profile.save()
            
            # notify_farmer_approval(farmer_profile)
            return Response({'message': f"Farmer {farmer_profile.user.username} approved."})
        except FarmerProfile.DoesNotExist:
            return Response({'error': 'Farmer profile not found.'}, status=404)


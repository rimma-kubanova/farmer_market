# from .models import Product
# from .permissions import IsFarmerOrReadOnly


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, FarmerProduct
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, ProductDetailSerializer
from .models import Product

class ProductNamesByCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category):
        valid_names = Product.PRODUCT_NAME_CHOICES.get(category, [])
        if not valid_names:
            return Response({"error": f"No valid product names found for category '{category}'."}, status=400)
        return Response({"category": category, "valid_names": valid_names})
    
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        # Use detailed serializer when retrieving a single product
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        # Farmer creates the product they sell
        product = serializer.save()
        FarmerProduct.objects.create(
            farmer=self.request.user,
            product=product,
            price=serializer.validated_data.get('price'),
            available_quantity=0  # Default value
        )

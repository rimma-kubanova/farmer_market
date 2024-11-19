# from .models import Product
# from .permissions import IsFarmerOrReadOnly


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, FarmerProduct
from .serializers import ProductSerializer, ProductDetailSerializer

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

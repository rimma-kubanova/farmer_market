from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductNamesByCategoryAPIView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('product-names/<str:category>/', ProductNamesByCategoryAPIView.as_view(), name='product-names-by-category'),
]
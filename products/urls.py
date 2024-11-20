from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView,
    ProductDetailView,
    FarmerProductListView,
    FarmerProductCreateView,
    FarmerProductUpdateView,
    FarmerProductDeleteView,
)

router = DefaultRouter()
# router.register('products', ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('my-products/', FarmerProductListView.as_view(), name='farmer-product-list'),
    path('my-products/create/', FarmerProductCreateView.as_view(), name='farmer-product-create'),
    path('my-products/<int:pk>/update/', FarmerProductUpdateView.as_view(), name='farmer-product-update'),
    path('my-products/<int:pk>/delete/', FarmerProductDeleteView.as_view(), name='farmer-product-delete'),
    # path('product-names/<str:category>/', ProductNamesByCategoryAPIView.as_view(), name='product-names-by-category'),
    
]
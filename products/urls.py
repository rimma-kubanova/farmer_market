from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    FarmerProductListView,
    FarmerProductCreateView,
    FarmerProductUpdateView,
    FarmerProductDeleteView,
    OrderListView,
    CartRemoveView,
    AddToCartView,
    ViewCartView,
    CheckoutCartView
)

router = DefaultRouter()
# router.register('products', ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),

    path('my-products/', FarmerProductListView.as_view(), name='farmer-product-list'),
    path('my-products/create/', FarmerProductCreateView.as_view(), name='farmer-product-create'),
    path('my-products/<int:pk>/update/', FarmerProductUpdateView.as_view(), name='farmer-product-update'),
    path('my-products/<int:pk>/delete/', FarmerProductDeleteView.as_view(), name='farmer-product-delete'),
    # path('product-names/<str:category>/', ProductNamesByCategoryAPIView.as_view(), name='product-names-by-category'),
    
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', ViewCartView.as_view(), name='view-cart'),     
    path('cart/checkout/', CheckoutCartView.as_view(), name='checkout-cart'),
    path('cart/remove/<int:farmer_product_id>/', CartRemoveView.as_view(), name='cart-remove'),
    
    path('order/', OrderListView.as_view(), name='order-list')
]
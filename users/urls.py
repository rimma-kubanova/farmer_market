from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UpdateBuyerProfileView, UpdateFarmerProfileView

router = DefaultRouter()
# router.register('users', UserViewSet)

urlpatterns = [
    path('register/<str:role>/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-buyer/', UpdateBuyerProfileView.as_view(), name='update-buyer'),
    path('update-farmere/', UpdateFarmerProfileView.as_view(), name='update-farmer'),
]
    # path('', include(router.urls)),
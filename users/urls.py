from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView

router = DefaultRouter()
# router.register('users', UserViewSet)

urlpatterns = [
    path('register/<str:role>/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('', include(router.urls)),
]
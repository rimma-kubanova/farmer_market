# from rest_framework.permissions import BasePermission

# class IsFarmerOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Allow read-only permissions for any request
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return True
#         # Write permissions are only allowed to the farmer who owns the product
#         return obj.farmer == request.user

from rest_framework.permissions import BasePermission

class IsFarmer(BasePermission):
    """
    Allow access only to users of type 'farmer'.
    """
    
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return request.user.is_authenticated and request.user.role == 'farmer'

class IsBuyerOrReadOnly(BasePermission):
    """
    Allow read-only access for buyers, but full access for farmers.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == 'farmer'

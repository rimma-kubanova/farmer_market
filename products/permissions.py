from rest_framework.permissions import BasePermission

class IsFarmerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for any request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Write permissions are only allowed to the farmer who owns the product
        return obj.farmer == request.user

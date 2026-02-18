from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # читать могут все
        if request.method in SAFE_METHODS:
            return True

        # писать только админ
        return request.user and request.user.is_staff

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

    
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
class IsManagerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["manager", "admin"]

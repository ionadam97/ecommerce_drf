from rest_framework.permissions import BasePermission



class IsUserCart(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user

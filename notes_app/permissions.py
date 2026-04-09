from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        owner_field = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        return owner_field == request.user or request.user.is_staff
from rest_framework.permissions import BasePermission


class IsOwnerUpateOrDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            if view.action == 'short_serializer':
                return True
            return obj.author == request.user.id
        return True

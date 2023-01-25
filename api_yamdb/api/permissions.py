from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return True
        if request.method == "DELETE":
            return request.user.is_superuser
        return (request.user.role == 'admin'
                or request.user.is_superuser)



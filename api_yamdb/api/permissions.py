from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method == 'PUT':
        #     return False
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        # if request.method == 'PUT':
        #     return False
        return (request.user.role == 'admin'
                or request.user.is_superuser)

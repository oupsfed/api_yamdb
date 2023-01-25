from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Редектирование разрешено только автору."""

    def has_object_permission(self, request, view, serializer):
        return (request.method in SAFE_METHODS
                or serializer.author == request.user)


class IsAdminOrReadOnly(BasePermission):
    """Редектирование разрешено только админу или модератору."""

    def has_object_permission(self, request, view, serializer):
        return (request.method in SAFE_METHODS
                or serializer.author.role == "moderator"
                or serializer.author.role == "admin")


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

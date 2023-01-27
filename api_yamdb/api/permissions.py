from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import status


class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            if not request.user.is_authenticated():
                raise GenericAPIException(detail="no auth", status_code=401)
            if not request.user.is_admin():
                raise GenericAPIException(detail="not admin", status_code=403)
            return True

        else:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin'
                or request.user.is_superuser)


class IsAdminAuthorOrReadOnly(BasePermission):
    """Редектирование разрешено только админу, автору или модератору."""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin'
                or request.user.is_superuser)


class IsAdminOrReadOnlyTitle(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return (request.user.role == 'admin'
                or request.user.is_superuser)

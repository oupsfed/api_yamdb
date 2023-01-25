from rest_framework import permissions
from rest_framework.exceptions import APIException
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


class UserPermission(permissions.BasePermission):

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

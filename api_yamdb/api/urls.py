from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


from .views import UserViewSet, auth, get_token, CategoryViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', auth, name='signup'),
    path('auth/token/', get_token, name='token'),
]

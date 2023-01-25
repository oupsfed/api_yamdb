from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .views import TitleViewSet, CategoryViewSet, GenreViewSet

from .views import UserViewSet, auth, get_token

router = routers.SimpleRouter()
router.register('users', UserViewSet)
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', auth, name='signup'),
    path('auth/token/', get_token, name='token'),
]

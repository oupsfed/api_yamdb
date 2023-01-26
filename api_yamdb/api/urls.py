from django.urls import include, path
from rest_framework.routers import SimpleRouter
# from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import (auth, CommentViewSet,
                       get_token, ReviewViewSet, UserViewSet)


router = SimpleRouter()
router.register('users', UserViewSet)
router.register('titles', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', auth, name='signup'),
    path('auth/token/', get_token, name='token'),
]

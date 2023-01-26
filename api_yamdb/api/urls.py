from django.urls import include, path
from rest_framework.routers import SimpleRouter
# from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (auth, CommentViewSet, get_token,
                    ReviewViewSet, UserViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet)




router = SimpleRouter()
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', auth, name='signup'),
    path('auth/token/', get_token, name='token'),
]

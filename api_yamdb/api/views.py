from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import mixins
#from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre
from .permissions import UserPermission
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleSerializer


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (UserPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('=category__username',)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (UserPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('=genre__username',)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)






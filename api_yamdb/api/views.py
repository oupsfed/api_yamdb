from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.permissions import ReadOnly, IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, ReviewSerializer)
from reviews.models import Review, Title


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def title_for_review(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title

    def get_queryset(self):
        return self.title_for_review().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_for_review()
        )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def review_for_comment(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review

    def get_queryset(self):
        return self.review_for_comment().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_for_comment()
        )

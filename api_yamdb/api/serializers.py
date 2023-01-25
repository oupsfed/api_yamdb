from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (ModelSerializer,
                                        SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
            )
        ]


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

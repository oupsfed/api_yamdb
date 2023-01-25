from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (ModelSerializer,
                                        SlugRelatedField,
                                        SerializerMethodField)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class TitleSerializer(ModelSerializer):
    raiting = SerializerMethodField()

    def get_raiting(self, obj):
        reviews_list = obj.reviews.all()
        raiting = 0
        for review in reviews_list:
            raiting += review.score
        return raiting


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

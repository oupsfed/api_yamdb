from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CurrentUserDefault,
                                        ModelSerializer,
                                        SlugRelatedField,
                                        SerializerMethodField)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254,
                                   required=True)
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]', )
    email = serializers.EmailField(max_length=254,
                                   )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя не может быть me!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]', )
    confirmation_code = serializers.CharField(max_length=512)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category

    def validate(self, data):
        if data['name'] == '' or type(data['name']) != str:
            raise serializers.ValidationError(
                'data not correct!')
        if data['slug'] == '' or type(data['slug']) != str:
            raise serializers.ValidationError(
                'data not correct!')
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category

    def validate(self, data):
        if data['name'] == '' or type(data['name']) != str:
            raise serializers.ValidationError(
                'data not correct!')
        if data['slug'] == '' or type(data['slug']) != str:
            raise serializers.ValidationError(
                'data not correct!')
        return data


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='username',
        read_only=True,
        # queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='username',
        read_only=True,
        # queryset=Genre.objects.all()
    )
    rating = SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_raiting(self, obj):
        reviews_list = obj.reviews.all()
        raiting = 0
        for review in reviews_list:
            raiting += review.score
        return raiting


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date',)
        model = Review
        # validators = [
        #    UniqueTogetherValidator(
        #       queryset=Title.objects.all(),
        #       fields=('title', 'author'),
        #    )
        #]


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

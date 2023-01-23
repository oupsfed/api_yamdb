from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class PostSerializer(serializers.ModelSerializer):
    #category = SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        fields = '__all__'
        model = Post

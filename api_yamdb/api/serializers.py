from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


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
    category = SlugRelatedField(slug_field='username', read_only=True, queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='username', read_only=True, queryset=Genre.objects.all())
     class Meta:
        fields = '__all__'
        model = Title

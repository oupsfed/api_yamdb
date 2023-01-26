from datetime import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
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
        exclude = ['id']
        model = Genre

    def validate(self, data):
        if data['name'] == '' or type(data['name']) != str:
            raise serializers.ValidationError(
                'data not correct!')
        if data['slug'] == '' or type(data['slug']) != str:
            raise serializers.ValidationError(
                'data not correct!')
        return data


class TitleSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(required=False)
    genre = GenreSerializer(required=False, many = True)

    class Meta:
        fields = '__all__'
        read_only_fields = ['rating']
        model = Title

    def validate(self, data):
        if data['name'] == '' or type(data['name']) != str:
            raise serializers.ValidationError(
                'name not correct!')
        if data['year'] == '' or type(data['year']) != int:
            raise serializers.ValidationError(
                'year not correct!')
        if data['year'] >= datetime.now():
            raise serializers.ValidationError('Check the year')
        if data['rating'] == '' or type(data['rating']) != int:
            raise serializers.ValidationError(
                'rating not correct!')
        if data['description'] == '' or type(data['description']) != str:
            raise serializers.ValidationError(
                'description not correct!')
        if data['category'] == '':
            raise serializers.ValidationError(
                'category not correct!')
        if data['genre'] == '':
            raise serializers.ValidationError(
                'genre not correct!')
        return data

    def create(self, validated_data):
        categories = validated_data.pop('category')
        genries = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for category in categories:
            current_category, status = Category.objects.get_or_create(
                **category)
            Title.objects.create(category=current_category, title=title)
        for genre in genries:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            Title.objects.create(category=current_genre, title=title)
        return title

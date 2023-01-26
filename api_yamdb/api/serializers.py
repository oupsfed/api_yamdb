from datetime import datetime
from rest_framework import serializers
from django.shortcuts import get_object_or_404

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
    genres = GenreSerializer(required=False, many=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ['rating']
        model = Title

    def validate(self, data):
        return data
        if data['name'] == '' or type(data['name']) != str:
            raise serializers.ValidationError(
                'name not correct!')
        if data['year'] == '' or type(data['year']) != int:
            raise serializers.ValidationError(
                'year not correct!')
        #if data['year'] >= datetime.now():
        #    raise serializers.ValidationError('Check the year')
        #if data['rating'] == '' or type(data['rating']) != int:
        #    raise serializers.ValidationError(
        #        'rating not correct!')
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
        category_slug = validated_data.pop('category')
        genre_slugs = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        #current_category = get_object_or_404(Category, slug=category_slug)
        #title.category = current_category
        #title.save()
        #for genre_slug in genre_slugs:
        #    current_genre = get_object_or_404(Genre, slug=genre_slug)
        #    title.genre.append(current_genre)
        #    title.save()
        return title

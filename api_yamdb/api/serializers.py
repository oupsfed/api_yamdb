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
    category = CategorySerializer(read_only=True, required=False)
    genre = GenreSerializer(read_only=True, required=False, many = True)
    #category = SlugRelatedField(slug_field='slug', read_only=True)  #, queryset=Category.objects.all())
    #genre = SlugRelatedField(slug_field='slug', read_only=True, many=True)   #, queryset=Genre.objects.all())

    class Meta:
        fields = '__all__'
        read_only_fields = ['rating']
        model = Title

    def validate(self, data):
        return data

    def create(self, validated_data):
        category_slug = None
        if 'category' in self.initial_data:
            category_slug = validated_data.pop('category')
        genre_slugs = []
        if 'genre' in self.initial_data:
            genre_slugs = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        return title

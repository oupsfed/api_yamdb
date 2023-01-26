from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


from reviews.models import Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre




class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year'),
                message='Данное произведение существует'
            )
        ]

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre = Genre.objects.get(
                    slug=genre.slug
                )
                GenreTitle.objects.create(
                    genre=current_genre, title=title
                )
            return title


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

    # def validate(self, data):
    #     if data['email']:
    #         if User.objects.filter(email=data['email']).exists():
    #             raise serializers.ValidationError(
    #                 'Имя не может быть me!')
    #     return data

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

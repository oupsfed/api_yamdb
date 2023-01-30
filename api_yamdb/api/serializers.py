from django.contrib.auth import get_user_model
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        EmailField, IntegerField,
                                        ModelSerializer, RegexField,
                                        SlugRelatedField, Serializer,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (Category, Comment, Genre,
                            GenreTitle, Review, Title)

User = get_user_model()


class UserSerializer(ModelSerializer):
    email = EmailField(max_length=254,
                       required=True)
    username = RegexField(max_length=150,
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


class AuthSerializer(ModelSerializer):
    username = RegexField(max_length=150,
                          regex=r'^[\w.@+-]', )
    email = EmailField(max_length=254,)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Имя не может быть me!')
        return value


class TokenSerializer(Serializer):
    username = RegexField(max_length=150,
                          regex=r'^[\w.@+-]', )
    confirmation_code = CharField(max_length=512)


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(ModelSerializer):
    genre = GenreSerializer(required=False, many=True)
    category = CategorySerializer()
    rating = IntegerField(read_only=True)
    year = IntegerField(required=False, allow_null=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',
                  'rating')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year'),
                message='Данное произведение существует'
            )
        ]


class CreateTitleSerializer(ModelSerializer):
    genre = SlugRelatedField(slug_field='slug',
                                        queryset=Genre.objects.all(),
                                        many=True,
                                        required=False)
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',)
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


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'title')
        model = Review

    def validate(self, obj):
        if (Review.objects.filter(
            title=self.context['view'].kwargs.get('title_id'),
            author=self.context['view'].request.user
        ).exists() and self.context['view'].request.method == 'POST'):
            raise ValidationError(
                'Ваш отзыв на это произведение уже существет'
            )
        return obj


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

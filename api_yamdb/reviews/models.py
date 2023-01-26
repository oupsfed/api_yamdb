# from email.headerregistry import Group
from django.db import models


# from .validators import validate_not_empty


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 related_name='title',
                                 verbose_name='category',
                                 help_text='CategoryTitle',
                                 on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name  # [:15]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}'

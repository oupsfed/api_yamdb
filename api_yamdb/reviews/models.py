from django.db import models

from users.models import User

SCORES = ((1, 1), (2, 2), (3, 3), (4, 4),
          (5, 5), (6, 6), (7, 7), (8, 8),
          (9, 9), (10, 10))


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
    name = models.CharField(
        'titles name',
        help_text='write titles name',
        max_length=256
    )
    year = models.DateField('titles year', auto_now_add=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='title',
        verbose_name='category',
        help_text='CategoryTitle',
        on_delete=models.CASCADE
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name='title',
        verbose_name='genre',
        help_text='GenreTitle'
    )

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(choices=SCORES)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('-pub_date',)

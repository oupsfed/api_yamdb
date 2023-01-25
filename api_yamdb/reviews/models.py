#from email.headerregistry import Group
from django.db import models


#from .validators import validate_not_empty


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
    name = models.CharField('titles name', help_text='write titles name', max_length=256)
                            #validators=[validate_not_empty])
    year = models.DateField('titles year', auto_now_add=True)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 related_name='title',
                                 verbose_name='category',
                                 help_text='CategoryTitle',
                                 on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre,
                              blank=True,
                              null=True,
                              related_name='title',
                              verbose_name='genre',
                              help_text='GenreTitle')

    class Meta:
        #ordering = ['-year']
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name  #[:15]

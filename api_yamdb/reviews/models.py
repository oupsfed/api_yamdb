#from email.headerregistry import Group
from django.db import models


#from .validators import validate_not_empty


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('titles name', help_text='write titles name')
                            #validators=[validate_not_empty])
    year =  models.DateTimeField('titles year', auto_now_add=True)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 related_name='title',
                                 verbose_name='category',
                                 help_text='categorys title')
    genre = models.ForeignKey(Genre,
                              blank=True,
                              null=True,
                              related_name='title',
                              verbose_name='genre',
                              help_text='genrys title')
    image = models.ImageField(
        'image',
        upload_to='title/',
        blank=True
    )

    class Meta:
        #ordering = ['-year']
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name  #[:15]

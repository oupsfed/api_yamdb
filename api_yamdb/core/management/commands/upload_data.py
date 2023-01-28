import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre,
                            GenreTitle, Review, Title,
                            User)


class Command(BaseCommand):
    help = 'Заполняет базу данных записями'

    def handle(self, *args, **kwargs):
        with open('static/data/category.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                data.save()
        with open('static/data/users.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                data.save()
        with open('static/data/titles.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category']),
                )
                data.save()
        with open('static/data/review.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                data.save()
        with open('static/data/comments.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    pub_date=row['pub_date']
                )
                data.save()
        with open('static/data/genre.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                data.save()
        with open('static/data/genre_title.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data = GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                data.save()

import csv

from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        with open('static/data/category.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
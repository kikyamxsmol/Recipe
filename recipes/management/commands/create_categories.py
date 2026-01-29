from django.core.management.base import BaseCommand
from recipes.models import Category

class Command(BaseCommand):
    help = 'Create default recipe categories'

    def handle(self, *args, **kwargs):
        categories = [
            ('Breakfast', 'breakfast'),
            ('Lunch', 'lunch'),
            ('Dinner', 'dinner'),
            ('Dessert', 'dessert'),
            ('Appetizer', 'appetizer'),
            ('Snack', 'snack'),
            ('Beverage', 'beverage'),
            ('Salad', 'salad'),
            ('Soup', 'soup'),
            ('Vegetarian', 'vegetarian'),
            ('Vegan', 'vegan'),
            ('Gluten-Free', 'gluten-free'),
        ]

        for name, slug in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                slug=slug
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category: {name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {name}')
                )
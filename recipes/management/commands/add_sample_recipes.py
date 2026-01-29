from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Ingredient, Instruction
from django.core.files.base import ContentFile
from io import BytesIO
import os

class Command(BaseCommand):
    help = 'Add sample recipes with placeholder images'

    def handle(self, *args, **options):
        # Create a sample user if not exists
        user, created = User.objects.get_or_create(
            username='chef',
            defaults={
                'email': 'chef@example.com',
                'first_name': 'Master',
                'last_name': 'Chef'
            }
        )
        if created:
            user.set_password('chef123')
            user.save()
            self.stdout.write(f"Created user: {user.username}")

        # Get or create category
        category, _ = Category.objects.get_or_create(
            slug='main-dishes',
            defaults={'name': 'Main Dishes'}
        )

        # Create a simple PNG placeholder image in memory
        # 1x1 transparent PNG
        png_bytes = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
            0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
            0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
            0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
            0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
            0x42, 0x60, 0x82
        ])

        # Sample recipes to create
        recipes_data = [
            {
                'title': 'Spaghetti Carbonara',
                'slug': 'spaghetti-carbonara',
                'description': 'Classic Italian pasta with creamy egg sauce and bacon.',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'easy',
            },
            {
                'title': 'Beef Stew',
                'slug': 'beef-stew',
                'description': 'Hearty beef stew with root vegetables and rich gravy.',
                'prep_time': 30,
                'cook_time': 120,
                'servings': 6,
                'difficulty': 'medium',
            },
            {
                'title': 'Chocolate Cake',
                'slug': 'chocolate-cake',
                'description': 'Decadent chocolate layer cake with frosting.',
                'prep_time': 20,
                'cook_time': 35,
                'servings': 8,
                'difficulty': 'medium',
            },
        ]

        for recipe_data in recipes_data:
            recipe, created = Recipe.objects.get_or_create(
                slug=recipe_data['slug'],
                defaults={
                    **recipe_data,
                    'author': user,
                    'category': category,
                }
            )
            
            if created:
                # Attach a placeholder image
                image_file = ContentFile(png_bytes, name=f"{recipe_data['slug']}.png")
                recipe.image.save(f"{recipe_data['slug']}.png", image_file, save=True)
                self.stdout.write(f"Created recipe: {recipe.title} with image")
            else:
                if not recipe.image:
                    # Update existing recipe without image
                    image_file = ContentFile(png_bytes, name=f"{recipe_data['slug']}.png")
                    recipe.image.save(f"{recipe_data['slug']}.png", image_file, save=True)
                    self.stdout.write(f"Updated recipe: {recipe.title} with image")
                else:
                    self.stdout.write(f"Recipe already has image: {recipe.title}")

        self.stdout.write(self.style.SUCCESS("Sample recipes and images added successfully!"))

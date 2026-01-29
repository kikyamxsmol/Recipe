
from django.contrib import admin
from .models import Category, Recipe, Ingredient, Instruction, Review, UserProfile

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'category', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [IngredientInline, InstructionInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    filter_horizontal = ['favorite_recipes']

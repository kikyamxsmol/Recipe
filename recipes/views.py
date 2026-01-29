from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Recipe, Category, Review, UserProfile, Ingredient, Instruction
from .forms import (
    RegisterForm, LoginForm, UserProfileForm,
    RecipeForm, IngredientFormSet, InstructionFormSet,
)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        instruction_formset = InstructionFormSet(request.POST, prefix='instructions')
        
        if form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            
            # Generate unique slug
            base_slug = slugify(recipe.title)
            slug = base_slug
            counter = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            recipe.slug = slug
            
            recipe.save()
            
            # Save ingredients
            ingredient_formset.instance = recipe
            ingredient_formset.save()
            
            # Save instructions
            instruction_formset.instance = recipe
            instruction_formset.save()
            
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        instruction_formset = InstructionFormSet(prefix='instructions')
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
    }
    return render(request, 'pages/add_recipe.html', context)

@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Check if user is the author
    if recipe.author != request.user:
        messages.error(request, 'You can only edit your own recipes.')
        return redirect('recipe_detail', slug=slug)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        instruction_formset = InstructionFormSet(request.POST, instance=recipe, prefix='instructions')
        
        if form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = form.save(commit=False)
            
            # Update slug if title changed
            if 'title' in form.changed_data:
                base_slug = slugify(recipe.title)
                slug = base_slug
                counter = 1
                while Recipe.objects.filter(slug=slug).exclude(pk=recipe.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                recipe.slug = slug
            
            recipe.save()
            ingredient_formset.save()
            instruction_formset.save()
            
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        instruction_formset = InstructionFormSet(instance=recipe, prefix='instructions')
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
        'recipe': recipe,
        'is_edit': True,
    }
    return render(request, 'pages/add_recipe.html', context)

@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    
    if recipe.author != request.user:
        messages.error(request, 'You can only delete your own recipes.')
        return redirect('recipe_detail', slug=slug)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipe_list')
    
    return render(request, 'pages/delete_recipe.html', {'recipe': recipe})

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'recipes': page_obj,
        'is_my_recipes': True,
    }
    return render(request, 'pages/recipe_list.html', context)


def recipe_list(request):
    recipes = Recipe.objects.all().select_related('category', 'author').prefetch_related('reviews')

    # Search by title or description
    query = request.GET.get('q', '').strip()
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    # Filter by category
    category_slug = request.GET.get('category', '').strip()
    if category_slug:
        recipes = recipes.filter(category__slug=category_slug)

    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '').strip()
    if difficulty and difficulty in [choice[0] for choice in Recipe.DIFFICULTY_CHOICES]:
        recipes = recipes.filter(difficulty=difficulty)

    # Filter by dietary restriction
    dietary = request.GET.get('dietary', '').strip()
    if dietary and dietary != 'none':
        recipes = recipes.filter(dietary_restriction=dietary)

    # Filter by prep time (max prep time)
    prep_time_max = request.GET.get('prep_time_max', '').strip()
    if prep_time_max:
        try:
            prep_time_max = int(prep_time_max)
            recipes = recipes.filter(prep_time__lte=prep_time_max)
        except (ValueError, TypeError):
            pass

    # Filter by total time (prep + cook)
    total_time_max = request.GET.get('total_time_max', '').strip()
    if total_time_max:
        try:
            total_time_max = int(total_time_max)
            recipes = recipes.filter(prep_time__lt=total_time_max).filter(cook_time__lt=total_time_max)
        except (ValueError, TypeError):
            pass

    # Filter by rating
    min_rating = request.GET.get('min_rating', '').strip()
    if min_rating:
        try:
            min_rating = int(min_rating)
            # Complex query for average rating filtering
            from django.db.models import Avg
            recipes = recipes.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)
        except (ValueError, TypeError):
            pass

    # Sort options
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        recipes = recipes.order_by('-created_at')
    elif sort_by == 'fastest':
        recipes = recipes.order_by('prep_time', 'cook_time')
    elif sort_by == 'title':
        recipes = recipes.order_by('title')
    elif sort_by == 'most_viewed':
        recipes = recipes.order_by('-view_count')
    elif sort_by == 'most_rated':
        from django.db.models import Count, Avg
        recipes = recipes.annotate(review_count=Count('reviews')).order_by('-review_count')

    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare filter context
    context = {
        'recipes': page_obj,
        'categories': Category.objects.all().order_by('name'),
        'dietary_options': Recipe.DIETARY_CHOICES,
        'query': query,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'selected_dietary': dietary,
        'selected_prep_time': prep_time_max,
        'selected_total_time': total_time_max,
        'selected_sort': sort_by,
        'selected_rating': min_rating,
    }
    return render(request, 'pages/recipe_list.html', context)


def dashboard(request):
    """Enhanced dashboard view with trending and recommended recipes"""
    from django.db.models import Avg, Count
    from datetime import timedelta
    from django.utils import timezone
    
    # Trending recipes (most viewed in last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    trending = Recipe.objects.filter(
        created_at__gte=thirty_days_ago
    ).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-view_count')[:6]
    
    # Top rated recipes
    top_rated = Recipe.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:6]
    
    # Recent recipes
    recent = Recipe.objects.all().order_by('-created_at')[:6]
    
    # Popular categories
    popular_categories = Category.objects.annotate(
        recipe_count=Count('recipe')
    ).order_by('-recipe_count')[:8]
    
    # If user is authenticated, get personalized recommendations
    recommended = None
    following_recipes = None
    if request.user.is_authenticated:
        # Recipes from followed users
        followed_users = request.user.profile.following.values_list('user_id', flat=True)
        following_recipes = Recipe.objects.filter(
            author_id__in=followed_users
        ).order_by('-created_at')[:6]
        
        # Recommended based on user's favorite categories
        user_favorite_categories = request.user.profile.favorite_recipes.values_list(
            'category_id', flat=True
        ).distinct()
        if user_favorite_categories:
            recommended = Recipe.objects.filter(
                category_id__in=user_favorite_categories
            ).exclude(
                id__in=request.user.profile.favorite_recipes.values_list('id', flat=True)
            ).annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')[:6]
    
    context = {
        'trending': trending,
        'top_rated': top_rated,
        'recent': recent,
        'popular_categories': popular_categories,
        'recommended': recommended,
        'following_recipes': following_recipes,
    }
    return render(request, 'pages/dashboard.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(
        Recipe.objects.select_related('category', 'author')
        .prefetch_related('ingredients', 'instructions', 'reviews'),
        slug=slug
    )
    
    # Increment view count
    recipe.view_count += 1
    recipe.save(update_fields=['view_count'])

    reviews = recipe.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'recipe': recipe,
        'ingredients': recipe.ingredients.all(),
        'instructions': recipe.instructions.all(),
        'reviews': reviews,
        'average_rating': average_rating,
        'reviews_count': reviews.count(),
        'rating_range': range(1, 6),
    }
    return render(request, 'pages/recipe_detail.html', context)


@login_required
def add_review(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Your review has been added!')
        return redirect('recipe_detail', slug=slug)

    return redirect('recipe_detail', slug=slug)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'pages/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            if '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    username = user_obj.username
                except User.DoesNotExist:
                    pass

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)

                messages.success(request, f'Welcome back, {user.username}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'pages/login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request, username=None):
    # If username is provided, show that user's profile; otherwise show current user's profile
    if username:
        profile = get_object_or_404(UserProfile, user__username=username)
    else:
        profile = request.user.profile

    if request.method == 'POST' and username is None:
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    elif username is None:
        # Prefill the form with profile instance and user fields via `user` kwarg
        form = UserProfileForm(instance=profile, user=request.user)
    else:
        form = None

    user_recipes = Recipe.objects.filter(author=profile.user)
    favorite_recipes = profile.favorite_recipes.all()

    context = {
        'profile': profile,
        'form': form,
        'user_recipes': user_recipes,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def toggle_favorite(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    profile = request.user.profile

    if recipe in profile.favorite_recipes.all():
        profile.favorite_recipes.remove(recipe)
        messages.success(request, f'{recipe.title} removed from favorites.')
    else:
        profile.favorite_recipes.add(recipe)
        messages.success(request, f'{recipe.title} added to favorites!')

    return redirect('recipe_detail', slug=slug)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile
    my_profile = request.user.profile
    if target_profile != my_profile:
        if my_profile in target_profile.followers.all():
            target_profile.followers.remove(my_profile)
            messages.info(request, f"You unfollowed {target_user.username}.")
        else:
            target_profile.followers.add(my_profile)
            messages.success(request, f"You are now following {target_user.username}!")
    return redirect('profile_detail', username=username)

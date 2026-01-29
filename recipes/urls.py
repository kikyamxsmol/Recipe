
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<slug:slug>/review/', views.add_review, name='add_review'),
    path('recipe/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('recipe/<slug:slug>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<slug:slug>/delete/', views.delete_recipe, name='delete_recipe'),
    
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/', views.profile_view, name='profile_detail'),
    path('profile/', views.profile_view, name='profile'),
]

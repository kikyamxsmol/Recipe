from recipes.models import Recipe
recipes = Recipe.objects.exclude(image='')
print('recipes with images:', recipes.count())
for r in recipes[:5]:
    print(f'{r.title}: {r.image.name if r.image else "empty"}')
all_recipes = Recipe.objects.all()
print(f'total recipes: {all_recipes.count()}')
for r in all_recipes[:3]:
    print(f'  {r.title}: image={r.image.name if r.image else "(none)"}')

from recipes.models import Recipe, Ingredient, Instruction

# Spaghetti Carbonara
recipe1 = Recipe.objects.get(slug='spaghetti-carbonara')
recipe1.ingredients.all().delete()
recipe1.instructions.all().delete()

ingredients_data = [
    {'name': 'Spaghetti', 'quantity': '400 g'},
    {'name': 'Bacon', 'quantity': '200 g'},
    {'name': 'Eggs', 'quantity': '4'},
    {'name': 'Parmesan cheese', 'quantity': '100 g'},
    {'name': 'Black pepper', 'quantity': 'to taste'},
    {'name': 'Salt', 'quantity': 'to taste'},
]

for i, ing_data in enumerate(ingredients_data):
    Ingredient.objects.create(
        recipe=recipe1,
        name=ing_data['name'],
        quantity=ing_data['quantity'],
        order=i
    )

instructions_data = [
    'Cook spaghetti in salted boiling water until al dente.',
    'Fry diced bacon until crispy, then set aside.',
    'Beat eggs with grated Parmesan cheese and black pepper.',
    'Drain pasta and toss with hot bacon and fat.',
    'Remove from heat and stir in egg mixture quickly.',
    'Serve immediately with extra Parmesan and black pepper.',
]

for i, desc in enumerate(instructions_data):
    Instruction.objects.create(
        recipe=recipe1,
        step_number=i+1,
        description=desc
    )

print(f"Added {recipe1.ingredients.count()} ingredients and {recipe1.instructions.count()} instructions to {recipe1.title}")

# Beef Stew
recipe2 = Recipe.objects.get(slug='beef-stew')
recipe2.ingredients.all().delete()
recipe2.instructions.all().delete()

ingredients_data = [
    {'name': 'Beef chuck', 'quantity': '1 kg, cubed'},
    {'name': 'Potatoes', 'quantity': '4 medium, diced'},
    {'name': 'Carrots', 'quantity': '3, sliced'},
    {'name': 'Onions', 'quantity': '2 medium, chopped'},
    {'name': 'Beef broth', 'quantity': '4 cups'},
    {'name': 'Tomato paste', 'quantity': '2 tbsp'},
    {'name': 'Olive oil', 'quantity': '3 tbsp'},
    {'name': 'Salt and pepper', 'quantity': 'to taste'},
]

for i, ing_data in enumerate(ingredients_data):
    Ingredient.objects.create(
        recipe=recipe2,
        name=ing_data['name'],
        quantity=ing_data['quantity'],
        order=i
    )

instructions_data = [
    'Brown beef chunks in hot olive oil, then remove.',
    'Sauté onions and carrots until softened.',
    'Add tomato paste and cook for 1 minute.',
    'Return beef to pot and add broth.',
    'Simmer for 90 minutes until beef is tender.',
    'Add potatoes and cook for 20 more minutes.',
    'Season with salt and pepper and serve.',
]

for i, desc in enumerate(instructions_data):
    Instruction.objects.create(
        recipe=recipe2,
        step_number=i+1,
        description=desc
    )

print(f"Added {recipe2.ingredients.count()} ingredients and {recipe2.instructions.count()} instructions to {recipe2.title}")

# Chocolate Cake
recipe3 = Recipe.objects.get(slug='chocolate-cake')
recipe3.ingredients.all().delete()
recipe3.instructions.all().delete()

ingredients_data = [
    {'name': 'All-purpose flour', 'quantity': '2 cups'},
    {'name': 'Cocoa powder', 'quantity': '3/4 cup'},
    {'name': 'Sugar', 'quantity': '1.5 cups'},
    {'name': 'Eggs', 'quantity': '3 large'},
    {'name': 'Butter', 'quantity': '1/2 cup, softened'},
    {'name': 'Milk', 'quantity': '1 cup'},
    {'name': 'Baking powder', 'quantity': '2 tsp'},
    {'name': 'Vanilla extract', 'quantity': '1 tsp'},
]

for i, ing_data in enumerate(ingredients_data):
    Ingredient.objects.create(
        recipe=recipe3,
        name=ing_data['name'],
        quantity=ing_data['quantity'],
        order=i
    )

instructions_data = [
    'Preheat oven to 350°F (175°C).',
    'Cream butter and sugar until light and fluffy.',
    'Beat in eggs one at a time.',
    'Mix flour, cocoa powder, and baking powder in a bowl.',
    'Alternate adding dry ingredients and milk to butter mixture.',
    'Stir in vanilla extract.',
    'Pour into greased pans and bake for 30-35 minutes.',
    'Cool and frost with chocolate frosting.',
]

for i, desc in enumerate(instructions_data):
    Instruction.objects.create(
        recipe=recipe3,
        step_number=i+1,
        description=desc
    )

print(f"Added {recipe3.ingredients.count()} ingredients and {recipe3.instructions.count()} instructions to {recipe3.title}")
print("Done!")

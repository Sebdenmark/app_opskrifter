import json
import random
import re

shown_recipes = []

def load_recipes(file_path):
    try:
        with open(file_path, "r") as file:
            recipes = json.load(file)
        return recipes
    except FileNotFoundError:
        print("Opskriftsfilen blev ikke fundet!")
        return []
    except json.JSONDecodeError:
        print("Der opstod en fejl under indlæsning af opskrifter!")
        return []

def get_random_recipe(recipes):
    global shown_recipes

    if not recipes:
        return "", "", "", ""

    if len(shown_recipes) == len(recipes):
        shown_recipes = []

    remaining_recipes = [recipe for recipe in recipes if recipe not in shown_recipes]

    if remaining_recipes:
        recipe = random.choice(remaining_recipes)
        shown_recipes.append(recipe)
        return recipe.get('title', ""), recipe.get('ingredients', ""), recipe.get('steps', ""), recipe.get('image_path', "")
    else:
        shown_recipes = []
        return get_random_recipe(recipes)

def filter_recipes_by_ingredients(recipes, selected_ingredients):
    filtered_recipes = []
    # Go through each recipe
    for recipe in recipes:
        recipe_ingredients = recipe['ingredients'].lower()
        if all(re.search(r'\b' + re.escape(ingredient.lower()) + r'\b', recipe_ingredients) for ingredient in selected_ingredients):
            filtered_recipes.append(recipe)
    random.shuffle(filtered_recipes)

    return filtered_recipes
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

def load_vegetarian_recipes(file_path):
    try:
        with open(file_path, "r") as file:
            recipes = json.load(file)
        return recipes
    except FileNotFoundError:
        print("Vegetar-opskriftsfilen blev ikke fundet!")
        return []
    except json.JSONDecodeError:
        print("Der opstod en fejl under indlæsning af vegetar-opskrifter!")
        return []

def get_random_recipe(recipes):
    global shown_recipes

    if not recipes:
        return "", "", "", ""

    # Hvis der ikke er opskrifter tilbage, nulstil shown_recipes og vælg en opskrift fra hele listen
    if len(shown_recipes) == len(recipes):
        shown_recipes = []

    # Find en opskrift, der ikke er blevet vist før
    remaining_recipes = [recipe for recipe in recipes if recipe not in shown_recipes]

    # Hvis der er opskrifter, der ikke er blevet vist, vælg en tilfældigt
    if remaining_recipes:
        recipe = random.choice(remaining_recipes)
        shown_recipes.append(recipe)

        # Returner opskriftens data
        return recipe.get('title', ""), recipe.get('ingredients', ""), recipe.get('steps', ""), recipe.get('image_path', "")
    else:
        # Hvis alle opskrifter er blevet vist, nulstil og start forfra
        shown_recipes = []
        return get_random_recipe(recipes)


def filter_recipes_by_ingredients(recipes, selected_ingredients):
    filtered_recipes = []

    # Go through each recipe
    for recipe in recipes:
        recipe_ingredients = recipe['ingredients'].lower()

        # Debugging output
        print(f"Checking recipe: {recipe['title']}")
        print(f"Recipe ingredients: {recipe_ingredients}")

        # Check if each selected ingredient exists in the recipe's ingredients
        # It will match only whole words, so "beef" won't match "beef stew"
        if all(re.search(r'\b' + re.escape(ingredient.lower()) + r'\b', recipe_ingredients) for ingredient in selected_ingredients):
            print(f"Selected ingredients found in: {recipe['title']}")
            filtered_recipes.append(recipe)

    return filtered_recipes
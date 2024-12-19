import json
import random

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
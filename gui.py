from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from recipe_logic import load_recipes, get_random_recipe, filter_recipes_by_ingredients
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.stencilview import StencilView


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add a background image
        self.background = Image(
            source='images/backgroundfrontpage.jpg',
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.background)

        # Main layout on top of the background
        self.main_layout = BoxLayout(orientation='vertical', padding=120, spacing=20)

        # Create a container for the welcome text
        welcome_container = BoxLayout(size_hint=(1, 0.4), padding=20, spacing=10)
        with welcome_container.canvas.before:
            Color(1, 1, 1, 0.7)  # Semi-transparent white background
            self.rect = Rectangle(size=welcome_container.size, pos=welcome_container.pos)
        welcome_container.bind(size=self._update_rect, pos=self._update_rect)

        # Label for forsiden
        self.welcome_label = Label(
            text="Hej! Hvad vil du lave i dag?\nVælg mellem almindelige og vegetariske opskrifter.\nEller vælg custom og få en opskrift der indenholder en eller flere af de ingredientser du har lyst til i dag.",
            bold=True,
            font_size=30,
            halign='center',
            valign='middle',
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'  # Path to your font file
        )
        welcome_container.add_widget(self.welcome_label)
        self.main_layout.add_widget(welcome_container)

        # Add buttons (unchanged)
        self.button_regular = Button(
            text="Dinner",
            bold=True,
            size_hint=(0.8, 0.15),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0.8, 0.85, 1, 1),
            font_size=30,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.button_regular.bind(on_press=self.go_to_recipe_regular)
        self.main_layout.add_widget(self.button_regular)

        self.button_vegetarian = Button(
            text="Vegan recipes",
            bold=True,
            size_hint=(0.8, 0.15),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(1, 0.85, 0.7, 1),
            font_size=30,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'

        )
        self.button_vegetarian.bind(on_press=self.go_to_recipe_vegetarian)
        self.main_layout.add_widget(self.button_vegetarian)

        self.button_lunch = Button(
            text="Lunch",
            bold=True,
            size_hint=(0.8, 0.15),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0.85, 1, 0.75, 1),
            font_size=30,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.button_lunch.bind(on_press=self.go_to_recipe_lunch)
        self.main_layout.add_widget(self.button_lunch)

        self.button_custom = Button(
            text="Custom Search",
            bold=True,
            size_hint=(0.8, 0.15),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(1, 0.75, 0.65, 1),
            font_size=30,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.button_custom.bind(on_press=self.go_to_custom_search)
        self.main_layout.add_widget(self.button_custom)

        self.add_widget(self.main_layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_to_recipe_regular(self, instance):
        self.manager.current = 'recipe'
        recipe_screen = self.manager.get_screen('recipe')
        recipe_screen.prepare_recipe("recipes.json")

    def go_to_recipe_vegetarian(self, instance):
        self.manager.current = 'recipe'
        recipe_screen = self.manager.get_screen('recipe')
        recipe_screen.prepare_recipe("vegetarian_recipes.json")

    def go_to_recipe_lunch(self, instance):
        self.manager.current = 'recipe'
        recipe_screen = self.manager.get_screen('recipe')
        recipe_screen.prepare_recipe("lunch.json")

    def go_to_custom_search(self, instance):
        self.manager.current = 'custom'

class CustomSearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_ingredients = []
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Add checkboxes for ingredient selection
        self.ingredient_options = ["beef", "carrots", "potatoes", "pasta", "cheese", "chicken", "rice", "shrimp"]
        self.checkboxes = {}
        for ingredient in self.ingredient_options:
            checkbox = Button(
                text=ingredient,
                size_hint=(1, 0.1),
                background_color=(0.8, 0.8, 0.8, 1),
                on_press=self.toggle_ingredient
            )
            self.checkboxes[ingredient] = checkbox
            self.main_layout.add_widget(checkbox)

        # Search button
        self.search_button = Button(
            text="Find Recipes",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=20
        )
        self.search_button.bind(on_press=self.find_recipes)
        self.main_layout.add_widget(self.search_button)

        # Back button
        self.back_button = Button(
            text="Back",
            size_hint=(1, 0.1),
            background_color=(0.8, 0.4, 0.2, 1),
            font_size=20
        )
        self.back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(self.back_button)
        self.add_widget(self.main_layout)

    def toggle_ingredient(self, instance):
        ingredient = instance.text
        if ingredient in self.selected_ingredients:
            self.selected_ingredients.remove(ingredient)
            instance.background_color = (0.8, 0.8, 0.8, 1)  # Gray color
        else:
            self.selected_ingredients.append(ingredient)
            instance.background_color = (0.2, 0.8, 0.4, 1)  # Green color

    def find_recipes(self, instance):
        # Load all three recipe files
        recipes = []
        recipes.extend(load_recipes("recipes.json"))
        recipes.extend(load_recipes("lunch.json"))
        recipes.extend(load_recipes("vegetarian_recipes.json"))
 # Debugging
        filtered_recipes = filter_recipes_by_ingredients(recipes, self.selected_ingredients)

        if not filtered_recipes:
            self.manager.get_screen("recipe").title_label.text = "No recipes found, press new recipe to get some random recipes for inspiration!"
        else:
            # Pass filtered recipes to the RecipeScreen and display the first recipe
            recipe_screen = self.manager.get_screen("recipe")
            recipe_screen.update_custom_recipes(filtered_recipes)
            # Set the first recipe from the filtered list
            recipe_screen.prepare_recipe_from_list(filtered_recipes)
        # Switch to the recipe screen
        self.manager.current = 'recipe'

    def go_back(self, instance):
        self.manager.current = 'welcome'
class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_recipe_file = "recipes.json"
        self.custom_recipes = []  # Store filtered recipes for Custom Search
        self.in_custom_mode = False  # Flag to check if in Custom Search mode

        # Main layout as a RelativeLayout to layer widgets
        self.main_layout = RelativeLayout()

        # Background image
        self.background_image = Image(
            source="images/opskriftbaggrund.jpg",  # Replace with your image filename
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.main_layout.add_widget(self.background_image)

        # Foreground layout for other content
        self.foreground_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label for the recipe title
        self.title_label = Label(
            text="Recipe Title",
            font_size=36,
            bold=True,
            size_hint=(1, 0.1),
            halign='center',
            valign='middle',
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.foreground_layout.add_widget(self.title_label)

        # Image widget for the recipe image
        self.image_widget = Image(size_hint=(1, 0.5))  # Space for the image
        self.foreground_layout.add_widget(self.image_widget)

        # ScrollView for ingredients and steps
        self.scrollview = ScrollView(size_hint=(1, 1))
        self.content_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.scrollview.add_widget(self.content_layout)

        # Steps and ingredients labels
        self.steps_label = Label(
            text="Steps:",
            font_size=30,
            bold=True,
            markup=True,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'

        )
        self.content_layout.add_widget(self.steps_label)

        self.ingredients_label = Label(
            text="Ingredients:",
            font_size=30,
            bold=True,
            markup=True,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.content_layout.add_widget(self.ingredients_label)

        # Add ScrollView to foreground layout
        self.foreground_layout.add_widget(self.scrollview)

        # Button to display a new recipe
        self.new_recipe_button = Button(
            text="New Recipe",
            bold=True,
            size_hint=(1, 0.1),
            background_color=(0.8, 0.85, 1, 1),
            font_size=30,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.new_recipe_button.bind(on_press=self.display_new_recipe)
        self.foreground_layout.add_widget(self.new_recipe_button)

        # Back button to go back to the WelcomeScreen
        self.back_button = Button(
            text="Back",
            bold=True,
            size_hint=(1, 0.1),
            background_color=(1, 0.75, 0.65, 1),
            font_size=30,
            color=(0.3, 0.15, 0.05, 1),
            font_name='txtstyle/OriginalSurfer-Regular.ttf'
        )
        self.back_button.bind(on_press=self.go_back)
        self.foreground_layout.add_widget(self.back_button)

        # Add foreground layout on top of the background
        self.main_layout.add_widget(self.foreground_layout)

        self.add_widget(self.main_layout)

    def update_custom_recipes(self, recipes):
        self.custom_recipes = recipes
        self.in_custom_mode = True  # Indicate Custom Search mode

    def prepare_recipe_from_list(self, recipes):
        if recipes:
            recipe = recipes[0]  # Display the first filtered recipe
            self.title_label.text = recipe.get('title', "")
            self.ingredients_label.text = f"[b][size=24]Ingredients:[/size][/b]\n\n" + "\n".join(
                recipe.get('ingredients', "").split(". "))
            self.steps_label.text = f"[b][size=24]Steps:[/size][/b]\n\n" + "\n".join(
                [f"Step {i + 1}: {step.strip()}" for i, step in enumerate(recipe.get('steps', "").split(". "))])

            if recipe.get('image_path'):
                self.image_widget.source = recipe.get('image_path')
            else:
                self.image_widget.source = ""
        else:
            self.title_label.text = "No recipe found"
            self.ingredients_label.text = ""
            self.steps_label.text = ""
            self.image_widget.source = ""

    def prepare_recipe(self, recipe_file=None):
        # Use the given file or fall back to the current file
        if recipe_file:
            self.current_recipe_file = recipe_file
        # Hide layout until the recipe is ready
        self.main_layout.opacity = 0
        # Get recipes from the file
        recipes = load_recipes(self.current_recipe_file)
        title, ingredients, steps, image_path = get_random_recipe(recipes)
        # Update recipe data
        self.update_recipe_content(title, ingredients, steps, image_path)
        # Animate layout to become visible
        animation = Animation(opacity=1, duration=1)
        animation.start(self.main_layout)

    def update_recipe_content(self, title, ingredients, steps, image_path):
        if title:
            self.title_label.text = title
        else:
            self.title_label.text = ""
        # Update image
        if image_path:
            self.image_widget.source = image_path
        else:
            self.image_widget.source = ""

        # Update ingredients and steps
        if ingredients:
            ingredients_list = ingredients.split(". ")
            ingredients_text = "\n".join([ingredient.strip() for ingredient in ingredients_list])
            self.ingredients_label.text = f"[b][size=24]Ingredients:[/size][/b]\n\n{ingredients_text}"
        else:
            self.ingredients_label.text = ""

        if steps:
            steps_list = steps.split(". ")
            steps_text = "\n".join([f"Step {i + 1}: {step.strip()}" for i, step in enumerate(steps_list)])
            self.steps_label.text = f"[b][size=24]Steps:[/size][/b]\n\n{steps_text}"
        else:
            self.steps_label.text = ""

    def display_new_recipe(self, instance):
        # Check if we are in Custom Search mode
        if self.in_custom_mode and self.custom_recipes:
            title, ingredients, steps, image_path = get_random_recipe(self.custom_recipes)
        else:
            # Use the default recipe file
            recipes = load_recipes(self.current_recipe_file)
            title, ingredients, steps, image_path = get_random_recipe(recipes)

        self.update_recipe_content(title, ingredients, steps, image_path)

    def go_back(self, instance):
        # Reset custom mode and switch back to WelcomeScreen
        self.in_custom_mode = False
        self.custom_recipes = []
        self.manager.current = 'welcome'

class RecipeApp(App):
    def build(self):
        screen_manager = ScreenManager()
        # Add screens
        screen_manager.add_widget(WelcomeScreen(name='welcome'))
        screen_manager.add_widget(RecipeScreen(name='recipe'))
        screen_manager.add_widget(CustomSearchScreen(name='custom'))

        return screen_manager
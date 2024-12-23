from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from recipe_logic import load_recipes, get_random_recipe


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label for forsiden
        self.welcome_label = Label(
            text="Hej! Hvad vil du lave i dag?\nVælg mellem almindelige og vegetariske opskrifter.",
            font_size=24,
            halign='center',
            valign='middle',
            size_hint=(1, 0.4)
        )
        self.main_layout.add_widget(self.welcome_label)

        # Knap til almindelige opskrifter
        self.button_regular = Button(
            text="Almindelige opskrifter",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=20
        )
        self.button_regular.bind(on_press=self.go_to_recipe_regular)
        self.main_layout.add_widget(self.button_regular)

        # Knap til vegetariske opskrifter
        self.button_vegetarian = Button(
            text="Vegetariske opskrifter",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.8, 0.4, 1),
            font_size=20
        )
        self.button_vegetarian.bind(on_press=self.go_to_recipe_vegetarian)
        self.main_layout.add_widget(self.button_vegetarian)

        self.button_dessert = Button(
            text="Desserter",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.4, 0.2, 1),
            font_size=20
        )
        self.button_dessert.bind(on_press=self.go_to_recipe_dessert)
        self.main_layout.add_widget(self.button_dessert)

        self.add_widget(self.main_layout)

    def go_to_recipe_regular(self, instance):
        self.manager.current = 'recipe'
        recipe_screen = self.manager.get_screen('recipe')
        recipe_screen.prepare_recipe("recipes.json")

    def go_to_recipe_vegetarian(self, instance):
        self.manager.current = 'recipe'
        recipe_screen = self.manager.get_screen('recipe')
        recipe_screen.prepare_recipe("vegetarian_recipes.json")

    def go_to_recipe_dessert(self, instance):
        self.manager.current = 'recipe'
        recipe_screen = self.manager.get_screen('recipe')
        recipe_screen.prepare_recipe("dessert_recipes.json")

class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_recipe_file = "recipes.json"  # Default file

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label for the recipe title
        self.title_label = Label(
            text="Recipe Title",
            font_size=36,
            bold=True,
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.main_layout.add_widget(self.title_label)

        # Image widget for the recipe image
        self.image_widget = Image(size_hint=(1, 0.5))  # Space for the image
        self.main_layout.add_widget(self.image_widget)

        # ScrollView for ingredients and steps
        self.scrollview = ScrollView(size_hint=(1, 1))
        self.content_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.scrollview.add_widget(self.content_layout)

        # Steps and ingredients labels
        self.steps_label = Label(
            text="Steps:",
            font_size=20,
            bold=True,
            markup=True
        )
        self.content_layout.add_widget(self.steps_label)

        self.ingredients_label = Label(
            text="Ingredients:",
            font_size=20,
            bold=True,
            markup=True
        )
        self.content_layout.add_widget(self.ingredients_label)

        # Add ScrollView to main layout
        self.main_layout.add_widget(self.scrollview)

        # Button to display a new recipe
        self.new_recipe_button = Button(
            text="New Recipe",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=20
        )
        self.new_recipe_button.bind(on_press=self.display_new_recipe)
        self.main_layout.add_widget(self.new_recipe_button)

        # Back button to go back to the WelcomeScreen
        self.back_button = Button(
            text="Back",
            size_hint=(1, 0.1),
            background_color=(0.8, 0.4, 0.2, 1),
            font_size=20
        )
        self.back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(self.back_button)

        self.add_widget(self.main_layout)

    def prepare_recipe(self, recipe_file=None):
        # Use the given file or fall back to the current file
        if recipe_file:
            self.current_recipe_file = recipe_file
        else:
            recipe_file = self.current_recipe_file

        # Hide layout until the recipe is ready
        self.main_layout.opacity = 0

        # Get recipes from the file
        recipes = load_recipes(recipe_file)
        title, ingredients, steps, image_path = get_random_recipe(recipes)

        # Update recipe data
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

        # Animate layout to become visible
        animation = Animation(opacity=1, duration=1)
        animation.start(self.main_layout)

    def display_new_recipe(self, instance):
        # Always use the active recipe file
        self.prepare_recipe()

    def go_back(self, instance):
        # Switch back to the WelcomeScreen
        self.manager.current = 'welcome'


class RecipeApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Tilføj skærme til ScreenManager
        screen_manager.add_widget(WelcomeScreen(name='welcome'))
        screen_manager.add_widget(RecipeScreen(name='recipe'))

        return screen_manager
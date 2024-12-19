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
            text="Hej! Så du ved ikke hvad du skal lave til aftensmad i dag?\nLad mig hjælpe dig, tryk på knappen under.",
            font_size=24,
            halign='center',
            valign='middle',
            size_hint=(1, 0.4)
        )
        self.main_layout.add_widget(self.welcome_label)

        # Knap til at finde en opskrift
        self.button = Button(
            text="Find en opskrift",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=20
        )
        self.button.bind(on_press=self.go_to_recipe)
        self.main_layout.add_widget(self.button)

        self.add_widget(self.main_layout)

    def go_to_recipe(self, instance):
        self.manager.current = 'recipe'  # Skift til opskriftskærmen
        self.manager.get_screen('recipe').prepare_recipe()  # Forbered opskriften før visning


class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label for opskriftens titel
        self.title_label = Label(
            text="Opskrift Titel",
            font_size=36,
            bold=True,
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.main_layout.add_widget(self.title_label)

        # Image widget til billede under titlen
        self.image_widget = Image(size_hint=(1, 0.5))  # Plads til billedet
        self.main_layout.add_widget(self.image_widget)

        # ScrollView til ingredienser og steps
        self.scrollview = ScrollView(size_hint=(1, 1))
        self.content_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.scrollview.add_widget(self.content_layout)

        # Fremgangsmåde og ingredienser
        self.steps_label = Label(
            text="Fremgangsmåde:",
            font_size=20,
            bold=True,
            markup=True
        )
        self.content_layout.add_widget(self.steps_label)

        self.ingredients_label = Label(
            text="Ingredienser:",
            font_size=20,
            bold=True,
            markup=True
        )
        self.content_layout.add_widget(self.ingredients_label)

        # Tilføj scrollview til recipe_layout
        self.main_layout.add_widget(self.scrollview)

        # Knap til at finde en ny opskrift
        self.new_recipe_button = Button(
            text="Ny opskrift",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=20
        )
        self.new_recipe_button.bind(on_press=self.display_new_recipe)
        self.main_layout.add_widget(self.new_recipe_button)

        self.add_widget(self.main_layout)

    def prepare_recipe(self):
        # Skjul layoutet indtil opskriften er klar
        self.main_layout.opacity = 0

        # Hent opskriften og opdater indholdet
        recipes = load_recipes("recipes.json")
        title, ingredients, steps, image_path = get_random_recipe(recipes)

        # Opdater opskriftens data
        if title:
            self.title_label.text = title
        else:
            self.title_label.text = ""

        # Opdater billede
        if image_path:
            self.image_widget.source = image_path
        else:
            self.image_widget.source = ""

        # Opdater ingredienser og fremgangsmåde, kun hvis de er tilgængelige
        if ingredients:
            ingredients_list = ingredients.split(". ")
            ingredients_text = "\n".join([ingredient.strip() for ingredient in ingredients_list])
            self.ingredients_label.text = f"[b][size=24]Ingredienser:[/size][/b]\n\n{ingredients_text}"
        else:
            self.ingredients_label.text = ""

        if steps:
            steps_list = steps.split(". ")
            steps_text = "\n".join([f"Step {i + 1}: {step.strip()}" for i, step in enumerate(steps_list)])
            self.steps_label.text = f"[b][size=24]Fremgangsmåde:[/size][/b]\n\n{steps_text}"
        else:
            self.steps_label.text = ""

        # Animer layoutet til at blive synligt
        animation = Animation(opacity=1, duration=1)
        animation.start(self.main_layout)

    def display_new_recipe(self, instance):
        self.prepare_recipe()


class RecipeApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Tilføj skærme til ScreenManager
        screen_manager.add_widget(WelcomeScreen(name='welcome'))
        screen_manager.add_widget(RecipeScreen(name='recipe'))

        return screen_manager
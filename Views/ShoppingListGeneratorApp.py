from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.textinput import TextInput
import re
import sys


class MainLayout(BoxLayout):
    pass


class Menu(BoxLayout):
    def display_sub_menu(self, category):
        self.clear_widgets()
        self.add_widget(SubMenu(category))


class SubMenu(BoxLayout):
    def __init__(self, category):
        self.category = category
        BoxLayout.__init__(self)

    def display_input_menu(self, action):
        self.clear_widgets()
        try:
            name_layout = re.sub(r'(?P<prefix>\w*)\s.*', r'\g<prefix>', action) + self.category.capitalize() + 'Layout'
            layout = eval('{}()'.format(name_layout))
            self.add_widget(layout)
        except TypeError:
            sys.stderr.write('Invalid type, the category must be wrong : {} '.format(self.category))


class CreateIngredientLayout(BoxLayout):
    pass


class DeleteIngredientLayout(BoxLayout):
    pass


class SetIngredientLayout(BoxLayout):
    pass


class DisplayIngredientLayout(BoxLayout):
    pass


class CreateMealLayout(BoxLayout):
    pass


class DeleteMealLayout(BoxLayout):
    pass


class SetMealLayout(BoxLayout):
    pass


class DisplayMealLayout(BoxLayout):
    pass


class CreateShoppingListLayout(BoxLayout):
    pass


class DeleteShoppingListLayout(BoxLayout):
    pass


class SetShoppingListLayout(BoxLayout):
    pass


class DisplayShoppingListLayout(BoxLayout):
    pass


class ShoppingListGeneratorApp(App):
    def build(self):
        init_main = MainLayout()
        init_main.add_widget(Menu())
        return init_main

slga = ShoppingListGeneratorApp().run()
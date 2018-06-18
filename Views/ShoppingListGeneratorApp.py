from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton


class MainButtonList(ListItemButton):
    pass


class MainMenuLayout(GridLayout):
    pass


class CreateIngredientLayout(GridLayout):
    pass


class DelIngredientLayout(GridLayout):
    pass


class SetIngredientLayout(GridLayout):
    pass


class DisplayIngredientLayout(GridLayout):
    pass


class CreateMealLayout(GridLayout):
    pass


class DelMealLayout(GridLayout):
    pass


class SetMealLayout(GridLayout):
    pass


class DisplayMealLayout(GridLayout):
    pass


class CreateShoppingListLayout(GridLayout):
    pass


class DelShoppingListLayout(GridLayout):
    pass


class SetShoppingListLayout(GridLayout):
    pass


class DisplayShoppingListLayout(GridLayout):
    pass


class ShoppingListGeneratorApp(App):
    def build(self):
        return
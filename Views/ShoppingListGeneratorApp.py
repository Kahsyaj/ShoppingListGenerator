from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from Controllers.IngredientManager import IngredientManager
from Controllers.MealManager import MealManager
from Controllers.RecipeManager import RecipeManager
import re
import sys


class MenuBehavior(BoxLayout):
    def __init__(self, category=None):
        self.category = category
        BoxLayout.__init__(self)

    def go_back_menu(self):
        self.clear_widgets()
        self.add_widget(Menu())


class InputMenuBehavior(MenuBehavior):
    def go_back_sub_menu(self):
        self.clear_widgets()
        self.add_widget(SubMenu(self.category))


class MainLayout(BoxLayout):
    pass


class Menu(BoxLayout):
    def display_sub_menu(self, category):
        self.clear_widgets()
        self.add_widget(SubMenu(category))


class SubMenu(MenuBehavior):
    def display_input_menu(self, action):
        self.clear_widgets()
        try:
            name_layout = re.sub(r'(?P<prefix>\w*)\s.*', r'\g<prefix>', action) + self.category.capitalize() + 'Layout'
            layout = eval('{}(self.category)'.format(name_layout))
            self.add_widget(layout)
        except TypeError:
            sys.stderr.write('Invalid type, the category must be wrong : {} '.format(self.category))



class CreateIngredientLayout(InputMenuBehavior):
    def create(self, name_ingredient):
        mgr = IngredientManager()
        mgr.db_create(name_ingredient)
        self.go_back_menu()


class DeleteIngredientLayout(InputMenuBehavior):
    pass


class SetIngredientLayout(InputMenuBehavior):
    pass


class DisplayIngredientLayout(InputMenuBehavior):
    pass


class CreateMealLayout(InputMenuBehavior):
    def create(self, name_meal):
        mgr = MealManager()
        meal = mgr.db_create(name_meal)
        self.clear_widgets()
        self.add_widget(AddRecipeLayout(meal.get_id()))


class DeleteMealLayout(InputMenuBehavior):
    pass


class SetMealLayout(InputMenuBehavior):
    pass


class DisplayMealLayout(InputMenuBehavior):
    pass


class CreateShoppingListLayout(InputMenuBehavior):
    pass


class DeleteShoppingListLayout(InputMenuBehavior):
    pass


class SetShoppingListLayout(InputMenuBehavior):
    pass


class DisplayShoppingListLayout(InputMenuBehavior):
    pass


class AddRecipeLayout(InputMenuBehavior):
    def __init__(self, id):
        self.id_meal = id
        InputMenuBehavior.__init__(self)

    def create(self, name_ing, qty):
        ing_mgr = IngredientManager()
        ing = ing_mgr.db_load(name=name_ing)
        if ing is None:
            ing = ing_mgr.db_create(name_ing)
        rcp_mgr = RecipeManager()
        rcp_mgr.db_create(self.id_meal, [[ing, int(qty)]])
        ing_lst = self.ids['ings_list']
        ing_n = self.ids['name_ingredient'].text
        ing_qty = self.ids['quantity'].text
        ing_lst.rows += 1
        ing_lst.add_widget(Label(text=ing_n))
        ing_lst.add_widget(Label(text=ing_qty))
        ing_n = ""
        ing_qty = ""


class DeleteRecipeLayout(InputMenuBehavior):
    pass


class SetRecipeLayout(InputMenuBehavior):
    pass


class DisplayRecipeLayout(InputMenuBehavior):
    pass


class ShoppingListGeneratorApp(App):
    def build(self):
        init_main = MainLayout()
        init_main.add_widget(Menu())
        return init_main

slga = ShoppingListGeneratorApp().run()
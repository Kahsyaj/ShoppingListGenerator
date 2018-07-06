from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.textinput import TextInput
from kivy.adapters.listadapter import ListAdapter
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from Models.Ingredient import Ingredient
from Models.Meal import Meal
from Models.Recipe import Recipe
from Models.ShoppingList import ShoppingList
from kivy.uix.listview import ListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from Controllers.IngredientManager import IngredientManager
from Controllers.MealManager import MealManager
from Controllers.RecipeManager import RecipeManager
from Controllers.ShoppingListManager import ShoppingListManager
from Controllers.Manager import Manager
import re
import sys
import string


class MenuBehavior(BoxLayout):
    def __init__(self, category=None):
        self.category = string.capwords(category).replace(' ', '') if ' ' in category else category.capitalize()
        BoxLayout.__init__(self)

    def go_back_menu(self):
        self.clear_widgets()
        self.add_widget(Menu())

    @staticmethod
    def get_widget(parent_widget, id):
        for widget in parent_widget.children:
            if widget.id == id:
                return widget

    @staticmethod
    def has_widget(parent_widget, id):
        for widget in parent_widget.children:
            if widget.id == id:
                return True
        return False


class InputMenuBehavior(MenuBehavior):
    def __init__(self, manager, category=None):
        self.manager = manager
        MenuBehavior.__init__(self, category)

    def go_back_sub_menu(self):
        self.clear_widgets()
        self.add_widget(SubMenu(self.category))


class MainLayout(BoxLayout):
    pass


class Menu(BoxLayout):
    def display_sub_menu(self, category):
        self.clear_widgets()
        sub_menu = SubMenu(category)
        elt_lst = ElementsList(category)
        elt_lst.display_items()
        sub_menu.add_widget(elt_lst)
        sub_menu.add_widget(BackCreateButtonsWidget())
        self.add_widget(sub_menu)


class SubMenu(MenuBehavior):
    def display_set_item_menu(self, id):
        self.clear_widgets()
        label = Label(text="Set {}".format(self.category), font_size=20, size_hint=(1, .3))
        self.add_widget(label)
        elt_lst = ElementsList(self.category)
        elt_lst.display_sets(id)
        self.add_widget(elt_lst)


class ElementsList(ScrollView):
    def __init__(self, category):
        self.category = string.capwords(category).replace(' ', '') if ' ' in category else category.capitalize()
        self.manager = eval(self.category + 'Manager()')
        ScrollView.__init__(self)

    def display_items(self):
        try:
            self.clear_widgets()
            items = self.manager.get_listview_info()
            lst = ItemsList()
            lst.id = 'list'
            for elt in items:
                lst.rows += 1
                for value in elt:
                    lst.add_widget(Label(text=str(value)))
                bloc = self.create_set_del_bloc(str(elt[0]))
                lst.add_widget(bloc)
            self.add_widget(lst)
        except TypeError:
            sys.stderr.write('Invalid type, the category must be wrong : {} '.format(self.category))

    def display_sets(self, id):
        self.clear_widgets()
        fields = self.manager.get_db_fields()
        grid_layout = SetsList(rows=len(fields))
        for field in fields:
            field = str(field[0])
            if 'id' not in field and 'deleted' not in field:
                grid_layout.add_widget(Label(text=field))
                grid_layout.add_widget(TextInput(text=self.manager.get_field(field, id)))
        self.add_widget(grid_layout)
        rmgr = RecipeManager()
        mgr = MealManager()
        meal = mgr.db_load(31)
        print(meal.recipe.to_dict())

    def del_item(self, id):
        self.manager.db_delete(id)
        self.display_items()

    def display_set_item(self, id):
        fields = self.manager.get_db_fields()
        self.reinit_lst()
        lst = self.ids['list']

    def create_set_del_bloc(self, id):
        button_block = GridLayout()
        button_block.cols = 2
        button_block.rows = 1
        set_button = Button(text="Set", id=id)
        set_button.bind(on_press=lambda a: self.parent.display_set_item_menu(set_button.id))
        del_button = Button(text="Del", id=id)
        del_button.bind(on_press=lambda a: self.del_item(del_button.id))
        button_block.add_widget(set_button)
        button_block.add_widget(del_button)
        return button_block


class ItemsList(GridLayout):
    pass


class SetsList(GridLayout):
    pass


class CreateIngredientLayout(InputMenuBehavior):
    def create(self, name_ingredient):
        self.manager.db_create(name_ingredient)
        self.go_back_menu()


class BackCreateButtonsWidget(GridLayout):
    pass


class DeleteIngredientLayout(InputMenuBehavior):
    pass


class SetIngredientLayout(ListView):
    pass


class DisplayIngredientLayout(InputMenuBehavior):
    pass


class CreateMealLayout(InputMenuBehavior):
    def create(self, name_meal):
        meal = self.manager.db_create(name_meal)
        self.clear_widgets()
        self.add_widget(AddRecipeLayout(RecipeManager(), 'recipe', meal.get_id()))


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
    def __init__(self, manager, category, id):
        self.id_meal = id
        InputMenuBehavior.__init__(self, manager, category)

    def create(self, name_ing, qty):
        ing_mgr = IngredientManager()
        ing = ing_mgr.db_load(name=name_ing)
        if ing is None:
            ing = ing_mgr.db_create(name_ing)
        self.manager.db_create(self.id_meal, [[ing, int(qty)]])
        ing_lst = self.ids['ings_list']
        ing_n = self.ids['name_ingredient'].text
        ing_qty = self.ids['quantity'].text
        ing_lst.rows += 1
        if MenuBehavior.has_widget(ing_lst, ing_n):
            MenuBehavior.get_widget(ing_lst, '{}_qty'.format(ing_n)).text = str(int(MenuBehavior.get_widget(ing_lst, '{}_qty'.format(ing_n)).text) + int(ing_qty))
        else:
            ing_lst.add_widget(Label(text=ing_n, id=ing_n))
            ing_lst.add_widget(Label(text=ing_qty, id='{}_qty'.format(ing_n)))
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

#mgr = Manager('')
#mgr.init_db()


slga = ShoppingListGeneratorApp().run()

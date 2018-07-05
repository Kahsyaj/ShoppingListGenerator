from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.textinput import TextInput
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.scrollview import ScrollView
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
        self.category = category
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
        elt_lst = ElementsList()
        elt_lst.display_items(category)
        sub_menu.add_widget(elt_lst)
        sub_menu.add_widget(BackCreateButtonsWidget())
        self.add_widget(sub_menu)


class SubMenu(MenuBehavior):
    def display_input_menu(self, action):
        self.clear_widgets()
        try:
            name_layout = re.sub(r'(?P<prefix>\w*)\s.*', r'\g<prefix>', action) + self.category.capitalize() + 'Layout'
            manager_name = self.category.capitalize() + 'Manager'
            layout = eval('{}({}(), self.category)'.format(name_layout, manager_name))
            self.add_widget(layout)
        except TypeError:
            sys.stderr.write('Invalid type, the category must be wrong : {} '.format(self.category))


class ElementsList(ScrollView):
    def display_items(self, category):
        try:
            category = string.capwords(category).replace(' ', '') if ' ' in category else category.capitalize()
            manager = eval(category + 'Manager()')
            items = manager.get_listview_info()
            lst = self.ids['list']
            print(items)
            for elt in items:
                print(elt)
                lst.rows += 1
                for key, value in elt.items():
                    print(value)
                    lst.add_widget(Label(text=str(value)))
                button_block = GridLayout()
                button_block.cols = 2
                button_block.rows = 1
                button_block.add_widget(Button(text="Set"))
                button_block.add_widget(Button(text="Del"))
                lst.add_widget(button_block)
        except TypeError:
            sys.stderr.write('Invalid type, the category must be wrong : {} '.format(category))

    def create_set_del_bloc

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

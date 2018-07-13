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

    @staticmethod
    def gen_blank_cells(widget, nb=1, size_hint=(1, 1)):
        for n in range(0, nb):
            widget.add_widget(Label(text="", size_hint=size_hint))


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
        elt_lst = ElementsList(self.category, id="elements_list")
        elt_lst.display_set(id)
        self.add_widget(elt_lst)
        button_block = BackSetPlusButtonsWidget() if self.category == 'Meal' else BackSetButtonsWidget()
        self.add_widget(button_block)

    def display_create_item_menu(self):
        self.clear_widgets()
        label = Label(text="Create {}".format(self.category), font_size=20, size_hint=(1, .3))
        self.add_widget(label)
        elt_lst = ElementsList(self.category, id="elements_list")
        elt_lst.display_create()
        self.add_widget(elt_lst)


class ElementsList(ScrollView):
    def __init__(self, category, **kwargs):
        self.category = category
        self.manager = eval(self.category + 'Manager()')
        self.managed = eval(self.category + "()")
        self.item_id = None
        ScrollView.__init__(self, **kwargs)

    def display_items(self):
        self.clear_widgets()
        items = self.manager.get_listview_info()
        lst = ItemsList()
        lst.id = 'item_list'
        for elt in items:
            lst.rows += 1
            for value in elt:
                lst.add_widget(Label(text=str(value)))
            bloc = self.create_set_del_bloc(str(elt[0]))
            lst.add_widget(bloc)
        self.add_widget(lst)

    def display_set_ingredient(self, id):
        self.clear_widgets()
        self.item_id = id
        self.managed = self.manager.db_load(id)
        fields = self.managed.to_dict()
        grid_layout = FieldsList(rows=len(fields), id="fields_list")
        for key, value in fields.items():
            grid_layout.add_widget(Label(text=key))
            grid_layout.add_widget(TextInput(id=key, text=str(value)))
        self.add_widget(grid_layout)

    def display_set_meal(self, id, load=True):
        self.clear_widgets()
        self.item_id = id
        if load:
            self.managed = self.manager.db_load(id)
        fields = self.managed.to_dict()
        cpt = 1
        rows_nb = len(fields)+(len(fields['recipe']['ingredients'])*len(fields['recipe']['ingredients'][0]))
        grid_layout = FieldsList(rows=rows_nb, cols=3, id="fields_list")
        for key, value in fields.items():
            grid_layout.add_widget(Label(text=key))
            if key != "recipe":
                grid_layout.add_widget(TextInput(id=key, text=str(value)))
                MenuBehavior.gen_blank_cells(grid_layout, size_hint=(0.1, 1))
            else:
                MenuBehavior.gen_blank_cells(grid_layout, nb=2, size_hint=(0.1, 1))
        for elt in fields['recipe']['ingredients']:
            elt['ingredient']['name_ingredient'] = '' if elt['ingredient']['name_ingredient'] is None else elt['ingredient']['name_ingredient']
            grid_layout.add_widget(Label(text='#{} name_ingredient'.format(str(cpt))))
            grid_layout.add_widget(TextInput(id='name_ingredient', text=elt['ingredient']['name_ingredient']))
            remove_button = Button(text='-', size_hint=(0.1, 1), id=elt['ingredient']['name_ingredient'])
            remove_button.bind(on_press=lambda n: self.del_set_meal_field(remove_button.id))
            grid_layout.add_widget(remove_button)
            grid_layout.add_widget(Label(text='quantity (grams)'))
            grid_layout.add_widget(TextInput(id='quantity', text=str(elt['quantity'])))
            MenuBehavior.gen_blank_cells(grid_layout, size_hint=(0.1, 1))
            cpt += 1
        self.add_widget(grid_layout)

    def del_set_meal_field(self, ing_name):
        self.managed.recipe.remove_ingredient(ing_name)
        rcp_mgr = RecipeManager()
        rcp_mgr.db_save(self.managed.recipe)
        self.display_set_meal(self.item_id)

    def add_set_meal_field(self):
        ing_mgr = IngredientManager()
        recipe_mgr = RecipeManager()
        tmp_ingredient = ing_mgr.db_create_temp_ingredient()
        recipe_mgr.db_create(self.item_id, [{'ingredient': tmp_ingredient, 'quantity': 0}])
        self.display_set_meal(self.item_id)

    def display_set(self, id):
        if self.category == 'Ingredient':
            self.display_set_ingredient(id)
        elif self.category == "Meal":
            self.display_set_meal(id)

    def display_create(self):
        self.clear_widgets()
        elements = self.managed.to_dict()
        grid_layout = FieldsList(rows=1, id="fields_list")
        for key, value in elements.items():
            if "id" in key or "deleted" in key:
                continue
            elif type(value) is not list and type(value) is not dict:
                grid_layout.add_widget(Label(text=key))
                grid_layout.add_widget(TextInput(id=key))
                grid_layout.rows += 1
            else:
                grid_layout.add_widget(Label(text=key))
                grid_layout.add_widget(Label(text=''))
                grid_layout.rows += 1
                for elt in value:
                    if type(elt) is list:
                        for itm in elt:
                            if type(itm) is dict:
                                for sec_key, sec_value in itm.items():
                                    if "id" in sec_key or "deleted" in sec_key:
                                        continue
                                    else:
                                        grid_layout.add_widget(Label(text=sec_key))
                                        grid_layout.add_widget(TextInput(id=sec_key))
                                        grid_layout.rows += 1
                            else:
                                grid_layout.add_widget(Label(text="Quantity (grams)"))
                                grid_layout.add_widget(TextInput(id="quantity"))
                                grid_layout.rows += 1
        self.add_widget(grid_layout)
        self.display_set_meal(self.item_id)

    def del_item(self, id):
        self.manager.db_delete(id)
        self.display_items()

    def set_item(self):
        if self.category == 'Ingredient':
            self.set_ingredient()
        elif self.category == 'Meal':
            self.set_meal()

    def set_ingredient(self):
        fields = MenuBehavior.get_widget(self, 'fields_list').children
        for elt in fields:
            if elt.id is None:
                continue
            else:
                self.managed.set_name_ingredient(elt.text)
                self.manager.db_save(self.managed)
        self.parent.parent.display_sub_menu(self.category)

    def set_meal(self):
        fields = MenuBehavior.get_widget(self, 'fields_list').children
        rcp_mgr = RecipeManager()
        cpt = len(self.managed.recipe.ingredients) - 1
        for elt in fields:
            if elt.id is None:
                continue
            elif elt.id == "quantity":
                self.managed.recipe.ingredients[cpt]['quantity'] = elt.text
            elif elt.id == "name_ingredient":
                self.managed.recipe.ingredients[cpt]['ingredient'].set_name_ingredient(elt.text)
                cpt -= 1
            elif elt.id == "name_meal":
                self.managed.set_name_meal(elt.text)
                self.manager.db_save(self.managed)
        rcp_mgr.db_save(self.managed.recipe)
        self.display_items()

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

    def go_back_and_delete_temp(self):
        ing_mgr = IngredientManager()
        rcp_mgr = RecipeManager()
        for ingredient in self.managed.recipe.ingredients:
            if ingredient['ingredient'].get_name_ingredient() is None:
                rcp_mgr.db_delete(self.item_id, ingredient['ingredient'].get_id_ingredient(), soft=False)
        ing_mgr.wash_temp_ingredient()
        self.parent.parent.display_sub_menu(self.category)

class ItemsList(GridLayout):
    pass


class FieldsList(GridLayout):
    pass


class CreateIngredientLayout(InputMenuBehavior):
    def create(self, name_ingredient):
        self.manager.db_create(name_ingredient)
        self.go_back_menu()


class BackCreateButtonsWidget(GridLayout):
    pass


class BackSetButtonsWidget(GridLayout):
    pass

class BackSetPlusButtonsWidget(GridLayout):
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

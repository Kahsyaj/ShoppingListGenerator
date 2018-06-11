#####################################################
# Class in charge of managing the menu interactions #
#####################################################
from IngredientManager import IngredientManager
from Models.Ingredient import Ingredient
from PurchaseManager import PurchaseManager
from RecipeManager import RecipeManager
from ShoppingListManager import ShoppingListManager
from MealManager import MealManager


class MenuController():
    def __init__(self, usr='root', psswd='root'):
        self.user = usr
        self.password = psswd

    def exec_add_ingredient(self, inputs):
        """
            Instanciate an ingredient manager to create the ingredient (depending on the values in inputs param : [{}])
            :param inputs: the values to the inputs from the menu
            :return: ing : the ingredient created
        """
        self.check_inputs_type(inputs)
        ing_mgr = IngredientManager(self.user, self.password)
        if not inputs[0].has_key('id_ingredient'):
            inputs[0]['id_ingredient'] = ing_mgr.get_current_id()
        ing = Ingredient().init(inputs)
        ing_mgr.db_create_from_obj(ing)
        return ing

        return ing_mgr.db_create(inputs[0]['name_ingredient'])

    def exec_add_meal(self, inputs):
        self.check_inputs_type(inputs)
        ml_mgr = MealManager(self.user, self.password)


    @classmethod
    def check_inputs_type(inputs):
        if type(inputs) is not list and type(inputs[0]) is not dict:
            raise TypeError('The parameter should be a dict')
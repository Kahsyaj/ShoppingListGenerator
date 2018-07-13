import copy
from Models.Ingredient import Ingredient

#################################################################################################
# Class representing a recipe for a specific meal composed by ingredients and quantities (grams #
#################################################################################################


class Recipe:

    def __init__(self, id_meal="0", ingredients=[{"ingredient": Ingredient(), "quantity": 0}]):
        self.id_meal = id_meal
        self.ingredients = ingredients
        self.deleted = 0

    def init(self, resp):
        """
            initialize a Recipe object from the result of a query (case when loading an object from db)
            :paramresp : the response to a select query returning the values to initialize the Purchase instance
            :return : the current instance
        """
        if not resp:
            raise ValueError('The result of the query is empty.')
        self.id_meal = resp[0]['id_meal']
        self.ingredients = []
        self.deleted = resp[0]['deleted']
        for elt in resp:
            self.ingredients.append({"ingredient": Ingredient().init([elt]), "quantity": elt['quantity']})
        return self

    # Getters and setters
    def get_id_meal(self):
        return self.id_meal

    def get_ingredients(self):
        return self.ingredients

    def get_deleted(self):
        return self.deleted

    def set_id_meal(self, new):
        self.id_meal = new

    def set_ingredients(self, new):
        self.ingredients = new

    def set_deleted(self, new):
        self.deleted = new

    def in_recipe(self, ingredient_name):
        """
            Return True if the ingredient is already in the recipe, else False
            :param ingredient_name : the name of the ingredient to check
            :return : True if the ingredient is in the recipe else False
        """
        answ = False
        for elt in self.ingredients:
            if ingredient_name == elt['ingredient'].get_name_ingredient():
                answ = True
                break
        return answ

    def add_ingredient(self, ingredient, qty):
        """
            Add an ingredient to the recipe
            :param ingredient : the ingredient to add
            :param qty : the quantity of the ingredient expressed in grams
            :return : True if success else False
        """
        done = False
        if not self.in_recipe(ingredient.get_name_ingredient()):
            self.ingredients.append({"ingredient": ingredient, "quantity": qty})
            done = True
        return done

    def remove_ingredient(self, ingredient_name):
        """
            Remove an ingredient from the recipe
            :param ingredient_name : the name of the ingredient to remove
            :return True if success else False
        """
        if not self.in_recipe(ingredient_name):
            return False
        for elt in self.ingredients:
            if ingredient_name == elt['ingredient'].get_name_ingredient():
                self.ingredients.remove(elt)
                return True

    def set_quantity(self, ingredient_name, new_qty):
        """
            Set the quantity of one ingredient from the recipe
            :param ingredient_name : the name of the ingredient to set
            :param new_qty : the new quantity to define
            :return : True if success else False
        """
        if not self.in_recipe(ingredient_name):
            return False
        for elt in self.ingredients:
            if ingredient_name == elt['ingredient'].get_name_ingredient():
                elt['quantity'] = new_qty
                return True

    def describe(self):
        """
            Display a representation of the object
        """
        print('---Recipe---\n')
        for elt in self.ingredients:
            elt['ingredient'].describe()
            print("---Quantity---\n{}\n".format(str(elt['quantity'])))

    def to_dict(self):
        """
        Returns the dict representation of the object
        :return: obj_dict : The dictionary representing the object
        """
        obj_dict = copy.deepcopy(self.__dict__)
        if 'id_meal' in obj_dict.keys():
            del obj_dict['id_meal']
        if 'deleted' in obj_dict.keys():
            del obj_dict['deleted']
        for ingredient in obj_dict['ingredients']:
            ingredient['ingredient'] = ingredient['ingredient'].to_dict() if type(ingredient['ingredient']) is not \
                                                                             dict else ingredient['ingredient']
        return obj_dict

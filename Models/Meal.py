####################################################################################
# Class representing a simple Meal composed with a name, and the recipe associated #
####################################################################################
from Models.Recipe import Recipe


class Meal:

    def __init__(self, id=0, name="", recipe=None):
        self.id_meal = id
        self.name_meal = str(name)
        self.recipe = recipe

    def init(self, resp):
        """
            initialize a Meal object from the result of a query (case when loading an object from db)
            :param resp : the response to a select query returning the values to initialize the Purchase instance
            :return : the current instance
        """
        if not resp:
            raise ValueError('The result of the query is empty.')
        self.id_meal = resp[0]['id_meal']
        self.name_meal = resp[0]['name_meal']
        self.recipe = Recipe().init(resp)
        return self

    # Getters and setters
    def get_id(self):
        return self.id_meal

    def get_name(self):
        return self.name_meal

    def get_recipe(self):
        return self.recipe

    def set_id(self, new):
        self.id_meal = new

    def set_name(self, new):
        self.name_meal = str(new)

    def set_recipe(self, new):
        self.recipe = new

    def describe(self):
        """
            Display a representation of the object
        """
        print("---Meal---\n{}".format(self.name_meal))
        self.recipe.describe()
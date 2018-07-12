import copy

####################################################################################
# Class representing a simple Meal composed with a name, and the recipe associated #
####################################################################################
from Models.Recipe import Recipe


class Meal:

    def __init__(self, id=0, name="", recipe=Recipe()):
        self.id_meal = id
        self.name_meal = str(name)
        self.recipe = recipe
        self.deleted = 0

    def init(self, resp):
        """
            initialize a Meal object from the result of a query (case when loading an object from db)
            :param resp : the response to a select query returning the values to initialize the Purchase instance
            :return: the current instance
        """
        if not resp:
            raise ValueError('The result of the query is empty.')
        self.id_meal = resp[0]['id_meal']
        self.name_meal = resp[0]['name_meal']
        self.recipe = Recipe().init(resp)
        self.deleted = resp[0]['deleted']
        return self

    # Getters and setters
    def get_id_meal(self):
        return self.id_meal

    def get_name_meal(self):
        return self.name_meal

    def get_recipe(self):
        return self.recipe

    def get_deleted(self):
        return self.deleted

    def set_id_meal(self, new):
        self.id_meal = new

    def set_name_meal(self, new):
        self.name_meal = str(new)

    def set_recipe(self, new):
        self.recipe = new

    def set_deleted(self, new):
        self.deleted = new

    def describe(self):
        """
            Display a representation of the object
        """
        print("---Meal---\n{}".format(self.name_meal))
        self.recipe.describe()

    def to_dict(self):
        obj_dict = copy.deepcopy(self.__dict__)
        if 'id_meal' in obj_dict.keys():
            del obj_dict['id_meal']
        if 'deleted' in obj_dict.keys():
            del obj_dict['deleted']
        obj_dict['recipe'] = obj_dict['recipe'].to_dict() if type(obj_dict['recipe']) is not dict else obj_dict['recipe']
        return obj_dict

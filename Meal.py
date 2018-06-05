####################################################################################
# Class representing a simple Meal composed with a name, and the recipe associated #
####################################################################################


class Meal:

    def __init__(self, id, name, recipe):
        self.id = id
        self.name = name
        self.recipe = recipe

    # Getters and setters
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_recipe(self):
        return self.recipe

    def set_id(self, new):
        self.id = new

    def set_name(self, new):
        self.name = str(new)

    def set_recipe(self, new):
        self.recipe = new

    def describe(self):
        print("---Meal---\n{}".format(self.name))
        self.recipe.describe()
#######################################################################################################
# Class representing a simple Meal composed with a name, and a list of Ingredients/quantities (grams) #
#######################################################################################################


class Meal:
    def __init__(self, name):
        self.name = name
        self.recipe = []

    # Getters and setters
    def get_name(self):
        return self.name

    def get_recipe(self):
        return self.recipe

    def set_name(self, new):
        self.name = str(new)

    def set_recipe(self, new):
        self.recipe = new

    """
    Return True if the ingredient is already in the recipe, else False
    :param ingredient_name : the name of the ingredient to check
    :return : True if the ingredient is in the recipe else False 
    """

    def in_recipe(self, ingredient_name):
        answ = True
        for elt in self.recipe:
            if ingredient_name == elt[0].get_name:
                answ = False
                break
        return answ

    """
    Add an ingredient to the recipe
    :param ingredient : the ingredient to add
    :param qty : the quantity of the ingredient expressed in grams
    :return : True if success else False
    """

    def add_ingredient(self, ingredient, qty):
        done = False
        if not self.in_recipe(ingredient.get_name):
            self.recipe.append([ingredient, qty])
            done = True
        return done

    """
    Remove an ingredient from the recipe
    :param ingredient_name : the name of the ingredient to remove
    :return True if success else False
    """

    def remove_ingredient(self, ingredient_name):
        for elt in self.recipe:
            if ingredient_name == elt[0].get_name:
                self.recipe.remove(elt)
                return True
        return False

    """
    Set the quantity of one ingredient from the recipe
    :param ingredient_name : the name of the ingredient to set
    :param new_qty : the new quantity to define
    :return : True if success else False
    """

    def set_quantity(self, ingredient_name, new_qty):
        if not self.in_recipe(ingredient_name):
            return False
        for elt in self.recipe:
            if ingredient_name == elt[0].get_name:
                elt[1] = new_qty
                return True

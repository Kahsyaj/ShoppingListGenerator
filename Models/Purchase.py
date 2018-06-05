###############################################################################################
# Class representing a list of ingredients and quantities to buy for a number of Meals chosen #
###############################################################################################


class Purchase:

    def __init__(self, id_shoppinglist, ingredients):
        self.id_shoppinglist = id_shoppinglist
        self.ingredients = ingredients

    # Getters and setters
    def get_id_shoppinglist(self):
        return self.id_shoppinglist

    def get_ingredients(self):
        return self.ingredients

    def set_id_shoppinglist(self, new):
        self.id_shoppinglist = new

    def set_ingredients(self, new):
        self.ingredients = new

    def in_purchase(self, ingredient_name):
        """
            Return True if the ingredient is already in the recipe, else False
            :param ingredient_name : the name of the ingredient to check
            :return : True if the ingredient is in the purchase else False
        """
        answ = True
        for elt in self.ingredients:
            if ingredient_name == elt[0].get_name:
                answ = False
                break
        return answ

    def add_ingredient(self, ingredient, qty):
        """
            Add an ingredient to the purchase
            :param ingredient : the ingredient to add
            :param qty : the quantity of the ingredient expressed in grams
            :return : True if success else False
        """
        done = False
        if not self.in_purchase(ingredient.get_name):
            self.ingredients.append([ingredient, qty])
            done = True
        return done

    def remove_ingredient(self, ingredient_name):
        """
            Remove an ingredient from the purchase
            :param ingredient_name : the name of the ingredient to remove
            :return True if success else False
        """
        if not self.in_purchase(ingredient_name):
            return False
        for elt in self.ingredients:
            if ingredient_name == elt[0].get_name:
                self.ingredients.remove(elt)
                return True

    def set_quantity(self, ingredient_name, new_qty):
        """
            Set the quantity of one ingredient from the purchase
            :param ingredient_name : the name of the ingredient to set
            :param new_qty : the new quantity to define
            :return : True if success else False
        """
        if not self.in_purchase(ingredient_name):
            return False
        for elt in self.ingredients:
            if ingredient_name == elt[0].get_name:
                elt[1] = new_qty
                return True

    def describe(self):
        """
            Display a representation of the object
        """
        for elt in self.ingredients:
            elt[0].describe()
            print("---Quantity---\n{}".format(str(elt[1])))
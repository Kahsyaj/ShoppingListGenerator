######################################################################################################
# Class representing a shoppingList containing ingredients and quantities from a number of Meals set #
######################################################################################################


class shoppingList:
    def __init__(self):
        self.list = {}

    def get_list(self):
        return self.list

    def set_list(self, new):
        self.list = new
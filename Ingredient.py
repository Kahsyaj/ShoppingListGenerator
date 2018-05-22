############################################################################
# Class representing a simple ingredient which could be affected to a Meal #
############################################################################

class Ingredient:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, new):
        self.name = str(new)
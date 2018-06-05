############################################################################
# Class representing a simple Ingredient which could be affected to a Meal #
############################################################################


class Ingredient:

    def __init__(self, id, name):
        self.id = id
        self.name = str(name)

    # Getters and setters
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_id(self, new):
        self.id = new

    def set_name(self, new):
        self.name = str(new)

    def describe(self):
        """
            Display a representation of the object
        """
        print("---Ingredient---\n{}".format(self.name))
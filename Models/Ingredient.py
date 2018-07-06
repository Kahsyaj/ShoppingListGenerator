############################################################################
# Class representing a simple Ingredient which could be affected to a Meal #
############################################################################


class Ingredient:

    def __init__(self, id=0, name=""):
            self.id_ingredient = id
            self.name_ingredient = name
            self.deleted = 0

    def init(self, resp):
        """
            initialize an Ingredient object from the result of a query (case when loading an object from db)
            :paramresp : the response to a select query returning the values to initialize the Ingredient instance
            :return : the current instance
        """
        if not resp:
            raise ValueError('The result of the query is empty.')
        self.id_ingredient = resp[0]['id_ingredient']
        self.name_ingredient = resp[0]['name_ingredient']
        self.deleted = resp[0]['deleted']
        return self

    # Getters and setters
    def get_id(self):
        return self.id_ingredient

    def get_name(self):
        return self.name_ingredient

    def get_deleted(self):
        return self.deleted

    def set_id(self, new):
        self.id_ingredient = new

    def set_name(self, new):
        self.name_ingredient = str(new)

    def set_deleted(self, new):
        self.deleted = new

    def describe(self):
        """
            Display a representation of the object
        """
        print("---Ingredient---\n{}".format(self.name_ingredient))

    def to_dict(self):
        return self.__dict__

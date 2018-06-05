######################################################################################################
# Class representing a shoppingList containing the purchases needed  a number of Meals set #
######################################################################################################


class shoppingList:

    def __init__(self, id, date, purchase):
        self.id = id
        self.date = date
        self.purchase = purchase

    # Getters and setters
    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_purchase(self):
        return self.purchase

    def set_id(self, new):
        self.id = new

    def set_date(self, new):
        self.date = new

    def set_purchase(self, new):
        self.purchase = new


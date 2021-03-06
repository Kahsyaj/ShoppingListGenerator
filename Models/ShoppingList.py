from Purchase import Purchase
from datetime import date


############################################################################################
# Class representing a shoppingList containing the purchases needed  a number of Meals set #
############################################################################################


class ShoppingList:

    def __init__(self, id=0, date=date.today(), purchase=Purchase()):
        self.id_shoppinglist = id
        self.date_shoppinglist = date
        self.purchase = purchase
        self.deleted = 0

    def init(self, resp):
        """
            initialize a ShoppingList object from the result of a query (case when loading an object from db)
            :param resp : the response to a select query returning the values to initialize the ShoppingList instance
            :return: the current instance
        """
        if not resp:
            raise ValueError('The result of the query is empty.')
        self.id_shoppinglist = resp[0]['id_shoppinglist']
        self.date_shoppinglist = resp[0]['date_shoppinglist']
        self.purchase = Purchase().init(resp)
        self.deleted = resp[0]['deleted']
        return self

    # Getters and setters
    def get_id_shoppinglist(self):
        return self.id_shoppinglist

    def get_date_shoppinglist(self):
        return self.date_shoppinglist

    def get_purchase(self):
        return self.purchase

    def get_deleted(self):
        return self.deleted

    def set_id_shoppinglist(self, new):
        self.id_shoppinglist = new

    def set_date_shoppinglist(self, new):
        self.date_shoppinglist = new

    def set_purchase(self, new):
        self.purchase = new

    def set_deleted(self, new):
        self.deleted = new


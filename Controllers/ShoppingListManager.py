#######################################################################################################
# Manager class of ShoppingList which deals with shopping lists saving / loading / setting / deleting #
#######################################################################################################
from Manager import Manager


class PurchaseManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        self.table = "Shoppinglists"
        Manager.__init__(self, self.table, usr, psswd)


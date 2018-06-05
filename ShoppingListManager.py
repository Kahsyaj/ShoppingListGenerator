#######################################################################################################
# Manager class of ShoppingList which deals with shopping lists saving / loading / setting / deleting #
#######################################################################################################
import Manager


class PurchaseManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        Manager.__init__(self, "shoppinglists", usr, psswd)


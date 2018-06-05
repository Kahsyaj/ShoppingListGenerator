##################################################################################################
# Manager class of Ingredient which deals with ingredients saving / loading / setting / deleting #
##################################################################################################
import Manager


class IngredientManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        Manager.__init__(self, "ingredients", usr, psswd)


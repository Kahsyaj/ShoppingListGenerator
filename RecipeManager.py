##########################################################################################
# Manager class of Recipe which deals with recipes saving / loading / setting / deleting #
##########################################################################################
import Manager


class RecipeManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        Manager.__init__(self, "recipes", usr, psswd)


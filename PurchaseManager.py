##############################################################################################
# Manager class of Purchase which deals with purchases saving / loading / setting / deleting #
##############################################################################################
import Manager


class PurchaseManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        Manager.__init__(self, "purchases", usr, psswd)


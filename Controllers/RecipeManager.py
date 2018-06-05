##########################################################################################
# Manager class of Recipe which deals with recipes saving / loading / setting / deleting #
##########################################################################################
from Manager import Manager
import mysql.connector as mariadb

class RecipeManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        self.table = "Recipe"
        Manager.__init__(self, self.table, usr, psswd)


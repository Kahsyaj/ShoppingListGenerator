##############################################################################################
# Manager class of Purchase which deals with purchases saving / loading / setting / deleting #
##############################################################################################
from Manager import Manager
from Models.Purchase import Purchase
import mysql.connector as mariadb
import sys


class PurchaseManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        self.table = "Purchase"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, id_shoppinglist, *ingredients):
        """
            Create a purchase in the database from an id_shoppinglist and a list of [Ingredient, quantity]
            :param id_shoppinglist : the id of the associated shoppinglist
            :param ingredients : the double list of [Ingredient, quantity] of the purchase
            :return : True if the purchase has been successfully created else, False
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(prepared=True)
        try:
            for ingredient in ingredients:
                cursor.execute("INSERT INTO `{}` (id_shoppinglist, id_ingredient, quantity) VALUES (?, ?, ?)".format(self.table),
                               (str(id_shoppinglist), str(ingredient[0].get_id()), str(ingredient[1])))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except:
            sys.stderr.write("An error occurred with the purchase creating.")
            return False
        return True

    def db_create(self, purchase):
        """
            Create a purchase in the database from a Purchase object
            :param purchase : the Purchase object to create in database
            :return : True if success else False
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(prepared=True)
        try:
            for ingredient in purchase.get_ingredients():
                cursor.execute("INSERT INTO `{}` (id_shoppinglist, id_ingredient, quantity) VALUES (?, ?, ?)"
                               .format(self.table), (purchase.get_id_shoppinglist(), ingredient[0].get_id(), ingredient[1]))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except:
            sys.stderr.write("An error occurred with the purchase creating.")
            return False
        return True

    def db_delete(self, id_shoppinglist):
        """
            Delete a purchase by its name or its id from the database (soft delete)
            :param  id_shoppinglist : the id of the Purchase to delete
            :return : False an error occurred else True
        """
        try:
            connect = Manager.get_connector(self)
            cursor = connect.cursor(prepared=True)
            cursor.execute("UPDATE `{}` SET deleted = 1 WHERE id_shoppinglist = %s".format(self.table), (id_shoppinglist,))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occurred with the purchase deleting.")
            return False
        return True

    def db_save(self, ingredient):
        """
            Save a purchase object into database
            :param ingredient : the object to save
            :return : False an error occurred else True
        """
        try:
            connect = Manager.get_connector(self)
            cursor = connect.cursor()
            cursor.execute("UPDATE `{}` SET name = %s WHERE id = %s".format(self.table), (ingredient.get_name(), str(ingredient.get_id())))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occured with the purchase saving.")
            return False
        return True

    def db_load(self, id=None, name=None):
        """
            From an id or a name, load an Ingredient object from the database
            :param id : the id of the ingredient to load
            :param name : the name of the ingredient to load
            :return : the Ingredient object loaded, None if not in database
        """
        if name is None and id is None:
            sys.stderr.write("No name or id mentioned.")
            return False
        else:
            connect = Manager.get_connector(self)
            cursor = connect.cursor(prepared=True)
            if id is not None:
                cursor.execute("SELECT * FROM `{}` WHERE id_ingredient = %s".format(self.table), (str(id),))
            else:
                cursor.execute("SELECT * FROM `{}` WHERE name_ingredient = %s".format(self.table), (name,))
            answ = cursor.fetchall()
            if answ is not None:
                answ = answ[0]
                return Ingredient(answ[0], answ[1])
            else:
                return None

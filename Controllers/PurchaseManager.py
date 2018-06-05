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
            Delete a purchase by its id_shoppinglist from the database (soft delete)
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

    def db_save(self, purchase):
        """
            Save a Purchase object into database
            :param purchase : the object to save
            :return : True if success, otherwise False
        """
        try:
            connect = Manager.get_connector(self)
            cursor = connect.cursor()
            for ingredient in purchase.get_ingredients():
                cursor.execute("UPDATE `{}` SET id_ingredient = %s, quantity = %s WHERE id_shoppinglist = %s".format(self.table),
                               (ingredient[0].get_id(), ingredient[1], purchase.get_id_shoppinglist()))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occurred with the object saving.")
            return False
        return True

    def db_load(self, id_shoppinglist):
        """
            From an id_shoppinglist, load a Purchase object from the database
            :param id_shoppinglist : the id of the purchase to load
            :return : the Purchase object loaded, None if not in database
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `{}` WHERE id_shoppinglist = {}".format(self.table, connect.escapte_string(id_shoppinglist)))
        answ = cursor.fetchall()
        if answ is not None:
            ing_lst = []
            id_s = answ[0][0]
            for elt in answ:
                ing_lst.append([elt[1], elt[2]])
            return Purchase(id_s, ing_lst)
        else:
            return None

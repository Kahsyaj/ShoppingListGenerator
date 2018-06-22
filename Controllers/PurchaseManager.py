##############################################################################################
# Manager class of Purchase which deals with purchases saving / loading / setting / deleting #
##############################################################################################
from Manager import Manager
from Models.Purchase import Purchase
import mysql.connector as mariadb
import pymysql
import sys


class PurchaseManager(Manager):

    def __init__(self, usr="toor", psswd="toor"):
        self.table = "Purchase"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, id, ingredients):
        """
            Create a purchase in the database from an id_shoppinglist and a list of [Ingredient, quantity]
            :param id : the id of the associated ShoppingList
            :param ingredients : the double list of [Ingredient, quantity] of the purchase
            :return: True if the purchase has been successfully created else, False
        """
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            for ingredient in ingredients:
                cursor.execute("INSERT INTO `{}` (id_shoppinglist, id_ingredient, quantity) VALUES (?, ?, ?)".format(self.table),
                               (str(id), str(ingredient[0].get_id()), str(ingredient[1])))
            connect.commit()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except:
            sys.stderr.write("An error occurred with the purchase creating.")
            return False
        connect.close()
        return True

    def db_create_from_obj(self, purchase):
        """
            Create a purchase in the database from a Purchase object
            :param purchase : the Purchase object to create in database
            :return: True if success else False
        """
        self.check_managed(purchase)
        connect = self.get_connector()
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
            :return: False an error occurred else True
        """
        try:
            connect = self.get_connector()
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
            :return: True if success, otherwise False
        """
        self.check_managed(purchase)
        try:
            connect = self.get_connector()
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

    def db_load(self, id):
        """
            From an id_shoppinglist, load a Purchase object from the database
            :param id : the id associated to the purchase to load
            :return: the Purchase object loaded, None if not in database
        """
        connect = self.get_connector()
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT Purchase.id_shoppinglist, Purchase.id_ingredient, Ingredient.name_ingredient FROM `{}` "
                       "INNER JOIN Ingredient ON Ingredient.id_ingredient = Purchase.id_ingredient "
                       "WHERE id_shoppinglist = {} AND Purchase.deleted = 0".format(self.table, pymysql.escape_string(str(id))))
        answ = cursor.fetchall()
        return Purchase().init(answ) if answ else None

    @staticmethod
    def check_managed(item):
        """
            Check if the parameter is from the type of the managed item, if not raise ValueError
            :param item : the item to verify
        """
        if type(item) is not Purchase:
            raise ValueError('The parameter must be a Purchase instance.')
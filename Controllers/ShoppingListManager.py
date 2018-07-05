#######################################################################################################
# Manager class of ShoppingList which deals with shopping lists saving / loading / setting / deleting #
#######################################################################################################
from Manager import Manager
from Models.ShoppingList import ShoppingList
from datetime import date
import mysql.connector as mariadb
import pymysql
import sys


class ShoppingListManager(Manager):

    def __init__(self, usr="toor", psswd="toor"):
        self.table = "ShoppingList"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, date=date.today()):
        """
            Create a ShoppingList in the database from a date
            :param date : the date of the shopping list
            :return: the ShoppingList object if successfully created else, False
        """
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            cursor.execute("INSERT INTO `{}` (date_shoppinglist) VALUES (?)".format(self.table), (date,))
            connect.commit()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except:
            sys.stderr.write("An error occurred with the purchase creating.")
            return False
        id = self.get_current_id() - 1
        connect.close()
        return ShoppingList(id, date)

    def db_create_from_obj(self, shoppinglist):
        """
            Create a purchase in the database from a Purchase object
            :param shoppinglist : the ShoppingLIst object to create in database
            :return: True if success else False
        """
        self.check_managed(shoppinglist)
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            cursor.execute("INSERT INTO `{}` (id_shoppinglist, date_shoppinglist) VALUES (?, ?)"
                            .format(self.table), (shoppinglist.get_id(), shoppinglist.get_date()))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may have a problem with the primary key.")
            return False
        except:
            sys.stderr.write("An error occurred with the shopping list creating.")
            return False
        return True

    def db_delete(self, id):
        """
            Delete a shopping list by its id from the database (soft delete)
            :param  id_shoppinglist : the id of the Purchase to delete
            :return: False an error occurred else True
        """
        try:
            connect = self.get_connector()
            cursor = connect.cursor(prepared=True)
            cursor.execute("UPDATE `{}` SET deleted = 1 WHERE id_shoppinglist = %s".format(self.table), (id,))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occurred with the shopping list deleting.")
            return False
        return True

    def db_save(self, shoppinglist):
        """
            Save a Purchase object into database
            :param shoppinglist : the object to save
            :return: True if success, otherwise False
        """
        self.check_managed(shoppinglist)
        try:
            connect = self.get_connector()
            cursor = connect.cursor()
            cursor.execute("UPDATE `{}` SET date_shoppinglist = %s WHERE id_shoppinglist = %s".format(self.table),
                           (shoppinglist.get_date(), shoppinglist.get_id()))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occurred with the object saving.")
            return False
        return True

    def db_load(self, id):
        """
            From an id_shoppinglist, load a ShoppingList object from the database
            :param id : the id of the shopping list to load
            :return: the ShoppingList object loaded, None if not in database
        """
        connect = self.get_connector()
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT ShoppingList.id_shoppinglist, ShoppingList.date_shoppinglist, Purchase.id_ingredient, "
                       "Purchase.quantity, Ingredient.name_ingredient FROM `{}` INNER JOIN Purchase "
                       "ON ShoppingList.id_shoppinglist = Purchase.id_shoppinglist INNER JOIN Ingredient "
                       "ON Purchase.id_ingredient = Ingredient.id_ingredient WHERE id_shoppinglist = {} "
                       "AND ShoppingList.deleted = 0".format(self.table, pymysql.escape_string(str(id))))
        answ = cursor.fetchall()
        connect.close()
        return ShoppingList().init(answ) if answ else None

    def get_listview_info(self):
        """
        Returns all the information from ShoppingList database (deleted = 0) formatted to display on ListView widget (id, date)
        :return: answ : The result of the query
        """
        connect = self.get_connector()
        cursor = connect.cursor(dictionary=True)
        cursor.execute('SELECT id_shoppinglist, date_shoppinglist FROM {} WHERE ShoppingList.deleted = 0'.format(self.table))
        answ = cursor.fetchall()
        connect.close()
        return answ

    def get_current_id(self):
        """
            Returns the current id, usefull to create associated objects in conformity with the database values
            and constraints
            :return: the current assignable id
        """
        connect = self.get_connector()
        cursor = connect.cursor()
        cursor.execute('SELECT MAX(id_shoppinglist) FROM {}'.format(self.table))
        connect.close()
        return int(cursor.fetchall()[0][0]) + 1

    @classmethod
    def check_managed(item):
        """
            Check if the parameter is from the type of the managed item, if not raise ValueError
            :param item : the item to verify
        """
        if type(item) is not ShoppingList:
            raise ValueError('The parameter must be a ShoppingList instance.')
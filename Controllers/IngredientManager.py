##################################################################################################
# Manager class of Ingredient which deals with ingredients saving / loading / setting / deleting #
##################################################################################################
from Manager import Manager
from Models.Ingredient import Ingredient
import mysql.connector as mariadb
import pymysql
import sys


class IngredientManager(Manager):

    def __init__(self, usr="toor", psswd="toor"):
        self.table = "Ingredient"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, name):
        """
            Create an ingredient in the database and get the max id to instanciate the associated object and returns it
            :param name : the name of the ingredient
            :return: the object ingredient corresponding to the one created in database if success else False
        """
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            cursor.execute("INSERT INTO `{}` (name_ingredient) VALUES (?)".format(self.table), (name,))
            connect.commit()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("The ingredient name \"{}\" may already exists.".format(name))
            return False
        except:
            sys.stderr.write("An error occurred with the ingredient creating.")
            return False
        id = self.get_current_id() - 1
        connect.close()
        return Ingredient(id, name)

    def db_create_from_obj(self, ingredient):
        """
            Create an ingredient in the database from a Ingredient object
            :param ingredient : the Ingredient object to create in database
            :return: True if success else False
        """
        self.check_managed(ingredient)
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            cursor.execute("INSERT INTO `{}` (id_ingredient, name_ingredient) VALUES (?, ?)"
                           .format(self.table), (ingredient.get_id_ingredient(), ingredient.get_name_ingredient()))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may have a problem with the primary key.")
            return False
        except:
            sys.stderr.write("An error occurred with the ingredient creating.")
            return False
        return True

    def db_delete(self, id=None, name=None):
        """
            Delete an ingredient by its name or its id from the database (soft delete)
            :param ? id : the id of the ingredient to delete
            :param ? name : the name of the ingredient to delete
            :return: False if no parameters given or if an error occurs else True
        """
        if name is None and id is None:
            sys.stderr.write("No name or id mentioned.")
            return False
        else:
            try:
                connect = self.get_connector()
                cursor = connect.cursor(prepared=True)
                if id is not None:
                    cursor.execute("UPDATE `{}` SET deleted = 1 WHERE id_ingredient = %s".format(self.table), (id,))
                else:
                    cursor.execute("UPDATE `{}` SET deleted = 1 WHERE name_ingredient = %s".format(self.table), (name,))
                connect.commit()
                connect.close()
            except:
                sys.stderr.write("An error occurred with the ingredient deleting.")
                return False
            return True

    def db_save(self, ingredient):
        """
            Save an Ingredient object into database
            :param ingredient : the object to save
            :return: False an error occurred else True
        """
        self.check_managed(ingredient)
        try:
            connect = self.get_connector()
            cursor = connect.cursor()
            cursor.execute('UPDATE `{}` SET `name_ingredient` = "{}" WHERE `id_ingredient` = {}'.format(self.table, ingredient.get_name_ingredient(), str(ingredient.get_id_ingredient())))
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
            :return: the Ingredient object loaded, None if not in database
        """
        if name is None and id is None:
            sys.stderr.write("No name or id mentioned.")
            return False
        else:
            connect = self.get_connector()
            cursor = connect.cursor(dictionary=True)
            if id is not None:
                cursor.execute("SELECT id_ingredient, name_ingredient, deleted FROM `{}` WHERE Ingredient.id_ingredient = {} "
                               "AND Ingredient.deleted = 0".format(self.table, pymysql.escape_string(str(id))))
            else:
                cursor.execute("SELECT id_ingredient, name_ingredient, deleted FROM `{}` WHERE Ingredient.name_ingredient = %s "
                               "AND Ingredient.deleted = 0".format(self.table), (name,))
            answ = cursor.fetchall()
            connect.close()
            return Ingredient().init(answ) if answ else None

    def get_listview_info(self):
        """
        Returns all the information from Ingredient database (deleted = 0) formatted to display on ListView widget (id, name)
        :return: answ : The result of the query
        """
        connect = self.get_connector()
        cursor = connect.cursor()
        cursor.execute('SELECT id_ingredient, name_ingredient FROM {} WHERE Ingredient.deleted = 0'.format(self.table))
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
        cursor.execute('SELECT MAX(id_ingredient) FROM {}'.format(self.table))
        connect.close()
        return int(cursor.fetchall()[0][0]) + 1

    @staticmethod
    def check_managed(item):
        """
            Check if the parameter is from the type of the managed item, if not raise ValueError
            :param item : the item to verify
        """
        if not isinstance(item, Ingredient):
            print(type(item))
            raise ValueError('The parameter must be an Ingredient instance.')
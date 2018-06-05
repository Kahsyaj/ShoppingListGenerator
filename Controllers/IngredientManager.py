##################################################################################################
# Manager class of Ingredient which deals with ingredients saving / loading / setting / deleting #
##################################################################################################
from Manager import Manager
from Models.Ingredient import Ingredient
import mysql.connector as mariadb
import sys


class IngredientManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        self.table = "Ingredient"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, name):
        """
            Create an ingredient in the database and get the max id to instanciate the associated object and returns it
            :param name : the name of the ingredient
            :return : the object ingredient corresponding to the one created in database if success else False
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(prepared=True)
        cursor_id = connect.cursor()
        try:
            cursor.execute("INSERT INTO `{}` (name_ingredient) VALUES (?)".format(self.table), (name,))
            connect.commit()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("The ingredient name \"{}\" already exists.".format(name))
            return False
        except:
            sys.stderr.write("An error occurred with the ingredient creating.")
            return False
        cursor_id.execute("SELECT MAX(id_ingredient) FROM `{}`".format(self.table))
        id = cursor_id.fetchall()[0][0]
        connect.close()
        return Ingredient(id, name)

    def db_delete(self, id=None, name=None):
        """
            Delete an ingredient by its name or its id from the database (soft delete)
            :param ? id : the id of the ingredient to delete
            :param ? name : the name of the ingredient to delete
            :return : False if no parameters given or if an error occurs else True
        """
        if name is None and id is None:
            sys.stderr.write("No name or id mentioned.")
            return False
        else:
            try:
                connect = Manager.get_connector(self)
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
            cursor = connect.cursor(dictionary=True)
            if id is not None:
                cursor.execute("SELECT * FROM `{}` WHERE id_ingredient = {}".format(self.table, connect.escape_string(id)))
            else:
                cursor.execute("SELECT * FROM `{}` WHERE name_ingredient = {}".format(self.table, connect.escape_string(name)))
            answ = cursor.fetchall()
            if answ is not None:
                answ = answ[0]
                return Ingredient(answ['id_ingredient'], answ['name_ingredient'])
            else:
                return None

#####################################################################################
# Manager class of Meal which deals with Meal saving / loading / setting / deleting #
#####################################################################################
from Manager import Manager
from Models.Meal import Meal
import mysql.connector as mariadb
import pymysql
import sys


class MealManager(Manager):

    def __init__(self, usr="toor", psswd="toor"):
        self.table = "Meal"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, name):
        """
            Create a meal in the database from a name
            :param name : the name of the meal
            :return: the Meal object if successfully created else, False
        """
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            cursor.execute("INSERT INTO `{}` (name_meal) VALUES (?)".format(self.table), (name,))
            connect.commit()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("The meal name {} may already exist.".format(name))
            return False
        except:
            sys.stderr.write("An error occurred with the meal creating.")
            return False
        id = self.get_current_id() - 1
        connect.close()
        return Meal(id, name)

    def db_create_from_obj(self, meal):
        """
            Create a recipe in the database from a Recipe object
            :param meal : the Recipe object to create in database
            :return: True if success else False
        """
        self.check_managed(meal)
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            cursor.execute("INSERT INTO `{}` (id_meal, name_meal) VALUES (?, ?)".format(self.table),
                           (meal.get_id(), meal.get_name()))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("The meal name {} or the meal id {} may already exist.".format(meal.get_name(), str(meal.get_id())))
            return False
        except:
            sys.stderr.write("An error occurred with the meal creating.")
            return False
        return True

    def db_delete(self, id=None, name=None):
        """
            Delete a meal by its name or its id from the database (soft delete)
            :param ? id : the id of the meal to delete
            :param ? name : the name of the meal to delete
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
                    cursor.execute("UPDATE `{}` SET deleted = 1 WHERE id_meal = %s".format(self.table), (id,))
                else:
                    cursor.execute("UPDATE `{}` SET deleted = 1 WHERE name_meal = %s".format(self.table), (name,))
                connect.commit()
                connect.close()
            except:
                sys.stderr.write("An error occurred with the meal deleting.")
                return False
            return True

    def db_save(self, meal):
        """
            Save a Meal object into database
            :param meal : the object to save
            :return: False an error occurred else True
        """
        self.check_managed(meal)
        try:
            connect = self.get_connector()
            cursor = connect.cursor()
            cursor.execute("UPDATE `{}` SET name_meal = %s WHERE id_meal = %s".format(self.table), (meal.get_name(), str(meal.get_id())))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occured with the meal saving.")
            return False
        return True

    def db_load(self, id=None, name=None):
        """
            From an id or a name, load a Meal object from the database
            :param id : the id of the meal to load
            :param name : the name of the meal to load
            :return: the Meal object loaded, None if not in database
        """
        if name is None and id is None:
            sys.stderr.write("No name or id mentioned.")
            return False
        else:
            connect = self.get_connector()
            cursor = connect.cursor(dictionary=True)
            if id is not None:
                cursor.execute("SELECT Meal.id_meal, Meal.name_meal, Recipe.id_ingredient, Ingredient.name_ingredient, "
                               "Recipe.quantity FROM `{}` INNER JOIN Meal ON Meal.id_meal = Recipe.id_meal INNER JOIN "
                               "Ingredient ON Recipe.id_ingredient = Ingredient.id_ingredient WHERE Meal.id_meal = {} "
                               "AND Recipe.deleted = 0".format(self.table, pymysql.escape_string(str(id))))
            else:
                cursor.execute("SELECT Meal.id_meal, Meal.name_meal, Recipe.id_ingredient, Ingredient.name_ingredient, "
                               "Recipe.quantity FROM `{}` INNER JOIN Meal ON Meal.id_meal = Recipe.id_meal INNER JOIN "
                               "Ingredient ON Recipe.id_ingredient = Ingredient.id_ingredient WHERE Meal.name_meal = {} "
                               "AND Recipe.deleted = 0".format(self.table, pymysql.escape_string(name)))
            answ = cursor.fetchall()
            connect.close()
            return Meal().init(answ) if answ else None

    def get_current_id(self):
        """
            Returns the current id, usefull to create associated objects in conformity with the database values
            and constraints
            :return: the current assignable id
        """
        connect = self.get_connector()
        cursor = connect.cursor()
        cursor.execute('SELECT MAX(id_meal) FROM {}'.format(self.table))
        connect.close()
        return int(cursor.fetchall()[0][0]) + 1

    @staticmethod
    def check_managed(item):
        """
            Check if the parameter is from the type of the managed item, if not raise ValueError
            :param item : the item to verify
        """
        if type(item) is not Meal:
            raise ValueError('The parameter must be a Meal instance.')

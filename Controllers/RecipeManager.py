##########################################################################################
# Manager class of Recipe which deals with recipes saving / loading / setting / deleting #
##########################################################################################
from Manager import Manager
from Models.Recipe import Recipe
import mysql.connector as mariadb
import pymysql
import sys


class RecipeManager(Manager):

    def __init__(self, usr="root", psswd="root"):
        self.table = "Recipe"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, id_meal, ingredients):
        """
            Create a purchase in the database from an id_shoppinglist and a list of [Ingredient, quantity]
            :paramid_meal : the id of the associated Meal
            :paramingredients : the double list of [Ingredient, quantity] of the recipe
            :return : True if the recipe has been successfully created else, False
        """
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            for ingredient in ingredients:
                cursor.execute("INSERT INTO `{}` (id_meal, id_ingredient, quantity) VALUES (?, ?, ?)".format(self.table),
                               (str(id_meal), str(ingredient[0].get_id()), str(ingredient[1])))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except:
            sys.stderr.write("An error occurred with the recipe creating.")
            return False
        return True

    def db_create_from_obj(self, recipe):
        """
            Create a recipe in the database from a Recipe object
            :paramrecipe : the Recipe object to create in database
            :return : True if success else False
        """
        self.check_managed(recipe)
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            for ingredient in recipe.get_ingredients():
                cursor.execute("INSERT INTO `{}` (id_meal, id_ingredient, quantity) VALUES (?, ?, ?)"
                               .format(self.table), (recipe.get_id_meal(), ingredient[0].get_id(), ingredient[1]))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except:
            sys.stderr.write("An error occurred with the recipe creating.")
            return False
        return True

    def db_delete(self, id_meal):
        """
            Delete a recipe by its id_meal from the database (soft delete)
            :param id_meal : the id of the Recipe to delete
            :return : False an error occurred else True
        """
        try:
            connect = self.get_connector()
            cursor = connect.cursor(prepared=True)
            cursor.execute("UPDATE `{}` SET deleted = 1 WHERE id_meal = %s".format(self.table), (id_meal,))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occurred with the recipe deleting.")
            return False
        return True

    def db_save(self, recipe):
        """
            Save a Recipe object into database
            :paramrecipe : the object to save
            :return : True if success, otherwise False
        """
        self.check_managed(recipe)
        try:
            connect = self.get_connector()
            cursor = connect.cursor()
            for ingredient in recipe.get_ingredients():
                cursor.execute("UPDATE `{}` SET id_ingredient = %s, quantity = %s WHERE id_meal = %s".format(self.table),
                               (ingredient[0].get_id(), ingredient[1], recipe.get_id_meal()))
            connect.commit()
            connect.close()
        except:
            sys.stderr.write("An error occurred with the object saving.")
            return False
        return True

    def db_load(self, id_meal):
        """
            From an id_meal, load a Recipe object from the database
            :paramid_meal : the id associated to the recipe to load
            :return : the Recipe object loaded, None if not in database
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT Recipe.id_meal, Recipe.id_ingredient, Ingredient.name_ingredient, Recipe.quantity "
                       "FROM `{}` INNER JOIN Ingredient ON Ingredient.id_ingredient = Recipe.id_ingredient WHERE "
                       "id_shoppinglist = {} AND Recipe.deleted = 0".format(self.table, pymysql.escape_string(str(id_meal))))
        answ = cursor.fetchall()
        return Recipe().init(answ)

    @staticmethod
    def check_managed(item):
        """
            Check if the parameter is from the type of the managed item, if not raise ValueError
            :paramitem : the item to verify
        """
        if type(item) is not Recipe:
            raise ValueError('The parameter must be a Recipe instance.')

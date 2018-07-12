##########################################################################################
# Manager class of Recipe which deals with recipes saving / loading / setting / deleting #
##########################################################################################
from Manager import Manager
from Models.Recipe import Recipe
import mysql.connector as mariadb
import pymysql
import sys


class RecipeManager(Manager):

    def __init__(self, usr="toor", psswd="toor"):
        self.table = "Recipe"
        Manager.__init__(self, self.table, usr, psswd)

    def db_create(self, id_meal, ingredients):
        """
            Create a recipe in the database from an id_meal and a list of [Ingredient, quantity]
            :paramid_meal : the id of the associated Meal
            :paramingredients : the double list of [Ingredient, quantity] of the recipe
            :return : True if the recipe has been successfully created else, False
        """
        connect = self.get_connector()
        cursor = connect.cursor(prepared=True)
        try:
            for ingredient in ingredients:
                existing = self.already_exist(id_meal, ingredient['ingredient'].get_id())
                if not existing:
                    cursor.execute("INSERT INTO `{}` (id_meal, id_ingredient, quantity) VALUES (?, ?, ?)".format(self.table),
                                   (str(id_meal), str(ingredient['ingredient'].get_id()), str(ingredient['quantity'])))
                else:
                    qty = existing[0][2] + ingredient[1]
                    cursor.execute("UPDATE `{}` SET quantity = %s WHERE id_meal = %s AND id_ingredient = %s".format(self.table),
                                   (str(qty), str(id_meal), str(ingredient['ingredient'].get_id())))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except mariadb.Error:
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
                               .format(self.table), (recipe.get_id_meal(), ingredient['ingredient'].get_id_ingredient(), ingredient['quantity']))
            connect.commit()
            connect.close()
        except mariadb.errors.IntegrityError:
            sys.stderr.write("You may forgot constraint on foreign keys.")
            return False
        except mariadb.Error:
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
        except mariadb.Error:
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
                print(ingredient['ingredient'].get_id_ingredient())
                print(ingredient['quantity'])
                print(recipe.get_id_meal())
                cursor.execute('UPDATE `{}` SET `id_ingredient` = "{}", `quantity` = "{}" WHERE `id_meal` = {}'
                               .format(self.table, ingredient['ingredient'].get_id_ingredient(), ingredient['quantity'],
                                       recipe.get_id_meal()))
            connect.commit()
            connect.close()
            return True
        except mariadb.Error:
            sys.stderr.write("An error occurred with the object saving.")
            return False

    def db_load(self, id_meal):
        """
            From an id_meal, load a Recipe object from the database
            :paramid_meal : the id associated to the recipe to load
            :return : the Recipe object loaded, None if not in database
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT Recipe.id_meal, Recipe.id_ingredient, Ingredient.name_ingredient, Recipe.quantity, Recipe.deleted "
                       "FROM `{}` INNER JOIN Ingredient ON Ingredient.id_ingredient = Recipe.id_ingredient WHERE "
                       "id_shoppinglist = {} AND Recipe.deleted = 0".format(self.table, pymysql.escape_string(str(id_meal))))
        answ = cursor.fetchall()
        connect.close()
        return Recipe().init(answ) if answ else None

    @staticmethod
    def check_managed(item):
        """
            Check if the parameter is from the type of the managed item, if not raise ValueError
            :paramitem : the item to verify
        """
        if not isinstance(item, Recipe):
            raise ValueError('The parameter must be a Recipe instance.')

    def already_exist(self, id_meal, id_ingredient):
        """
            From an id_meal and an id_ingredient, return the element loaded if exists else False
            :param id_meal: the id_meal of the recipe
            :param id_ingredient: the id ingredient of the recipe
            :return: the informations of the recipe if exists else False
        """
        connect = Manager.get_connector(self)
        cursor = connect.cursor(prepared=True)
        cursor.execute("SELECT * FROM `{}` WHERE id_meal = %s AND id_ingredient = %s".format(self.table),
                       (str(id_meal), str(id_ingredient)))
        answ = cursor.fetchall()
        connect.close()
        return False if not answ else answ

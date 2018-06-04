################################################################################
# Manager class which deals with objects saving / loading / setting / deleting #
################################################################################
import pickle
import re
import os
import mysql.connector as mariadb


class Manager:
    """
    Manager constructor - May have both mode further for offline use
    :param mode : Defines if save are managed into file or in database
    """
    def __init__(self, mode="file", usr="root", psswd="root"):
        self.mode = mode
        if mode == "file":
            self.folder = "../ShpLstSave/"
            self.ext = ".bak"
        elif mode == "database":
            self.database = "ShoppingListGenerator"
            self.user = usr
            self.password = psswd
            self.tables = []
        else:
            raise ValueError('You can only choose between "file" and "database".')

    # Getters and setters
    def get_folder(self):
        return self.folder

    def get_database(self):
        return self.database

    def get_tables(self):
        return self.tables

    def get_ext(self):
        return self.ext

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def set_folder(self, new):
        self.folder = new

    def set_database(self, new):
        self.database = new

    def set_tables(self, new):
        self.tables = new

    def set_ext(self, new):
        self.ext = new

    def set_user(self, new):
        self.user = new

    def set_password(self, new):
        self.password = new

    """
    From an object, generate a file name (based on the type of the object and it's name) for saving / managing
    :param obj : the object from which generate the name
    """
    def gen_file_name_from_obj(self, obj):
        return re.sub(r"'(?P<name>[\w]*)'", r"\g<name>" + "_{}{}".format(obj.get_name(), self.ext), type(obj))

    """
    From an object, generate the associated table name
    :param obj : the object from which generate the name
    """
    def gen_table_name_from_obj(self, obj):
        return re.sub(r"'(?P<name>[\w]*)'", r"\g<name>", type(obj))

    """
    Save an object (Serialize) into a file (name given with gen_file_name_from_obj()
    :param : obj : the object to save
    """
    def file_save(self, obj):
        with open(self.gen_file_name_from_obj(obj), "wb") as f:
            pickle.dump(obj, f)

    """
    From a file name, load the associated object and returns it
    :param file_name : the name of the file to load
    :return : the object loaded
    """
    def file_load(self, file_name):
        with open(self.folder + file_name, "rb") as f:
            return pickle.load(f)

    """
    Load all the objects from the dest directory into a dict and returns it
    :return objs : the dictionary containing the objects loaded
    """
    def files_load(self):
        objs = dict()
        for file in os.listdir(self.folder):
            with open(self.folder + file, "rb") as f:
                obj = pickle.load(f)
                objs[file] = obj
        return objs

    """
    Creates all tables for the database to store ingredients, recipes ect...
    """
    def init_db(self):
        mariadb_connect = mariadb.connect(user=self.user, password=self.password, database=self.dest)
        cursor = mariadb_connect.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Ingredient (id_ingredient INT NOT NULL AUTO_INCREMENT, name_ingredient VARCHAR(50), deleted INT(1) DEFAULT 0, "
            "UNIQUE (name_ingredient), CONSTRAINT Ingredient_PK PRIMARY KEY (id_ingredient)) ENGINE=InnoDB")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Meal (id_meal INT NOT NULL AUTO_INCREMENT, name_meal VARCHAR(50), deleted INT(1) DEFAULT 0, "
            "UNIQUE (name_meal), CONSTRAINT Meal_PK PRIMARY KEY (id_meal)) ENGINE=InnoDB")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Recipe (id_ingredient INT NOT NULL, id_meal INT NOT NULL, quantity INT, "
            "deleted INT(1) DEFAULT 0, CONSTRAINT Recipe_PK PRIMARY KEY (id_meal,id_ingredient), "
            "CONSTRAINT Recipe_Meal_FK FOREIGN KEY (id_meal) REFERENCES Meal(id_meal), "
            "CONSTRAINT Recipe_Ingredient0_FK FOREIGN KEY (id_ingredient) REFERENCES Ingredient(id_ingredient)) ENGINE=InnoDB")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS ShoppingList (id_shoppinglist INT NOT NULL AUTO_INCREMENT, date_shoppinglist DATE, "
            "quantity INT, deleted INT(1) DEFAULT 0, CONSTRAINT ShoppingList_PK PRIMARY KEY (id_shoppinglist)) ENGINE=InnoDB"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Purchase ( id_ingredient INT NOT NULL, id_shoppinglist Int NOT NULL, "
            "quantity INT NOT NULL, CONSTRAINT Purchase_PK PRIMARY KEY (id_ingredient,id_shoppinglist), "
            "CONSTRAINT Purchase_Ingredient_FK FOREIGN KEY (id_ingredient) REFERENCES Ingredient(id_ingredient), "
            "CONSTRAINT Purchase_ShoppingList0_FK FOREIGN KEY (id_shoppinglist) REFERENCES ShoppingList(id_shoppinglist)) ENGINE=InnoDB"
        )

    """
    """
    def db_save(self, obj):
        mariadb_connect = mariadb.connect(user=self.user, password=self.password, database=self.dest)
        cursor = mariadb_connect.cursor(Prepared=True)
        cursor.execute
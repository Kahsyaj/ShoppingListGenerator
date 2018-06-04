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
            self.dest = "../ShpLstSave/"
            self.ext = ".bak"
        elif mode == "database":
            self.dest = "ShoppingList"
            self.user = usr
            self.password = psswd
            self.tables = []
        else:
            raise ValueError('You can only choose between "file" and "database".')

    # Getters and setters
    def get_dest(self):
        return self.dest

    def get_tbls(self):
        return self.tbls

    def get_ext(self):
        return self.ext

    def set_dest(self, new):
        self.dest = new

    def set_tbls(self, new):
        self.tbls = new

    def set_ext(self, new):
        self.ext = new

    """
    From an object, generate a file name (based on the type of the object and it's name) for saving / managing
    :param obj : the object from which generate the name
    """
    def gen_file_name_from_obj(self, obj):
        return re.sub(r"'(?P<name>[\w]*)'", r"\g<name>" + "_{}{}".format(obj.get_name(), self.ext), type(obj))

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
        with open(self.dest + file_name, "rb") as f:
            return pickle.load(f)

    """
    Load all the objects from the dest directory into a dict and returns it
    :return objs : the dictionary containing the objects loaded
    """
    def files_load(self):
        objs = dict()
        for file in os.listdir(self.dest):
            with open(self.dest + file, "rb") as f:
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

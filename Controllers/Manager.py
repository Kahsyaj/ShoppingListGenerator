################################################################################
# Manager class which deals with objects saving / loading / setting / deleting #
################################################################################
import pickle
import re
import os
import mysql.connector as mariadb


class Manager:
    def __init__(self, folder, usr="toor", psswd="toor", host='localhost'):
        self.folder = "../Save/{}/".format(folder)
        self.ext = ".bak"
        self.database = "ShoppingListGenerator"
        self.user = usr
        self.password = psswd
        self.host = host

    # Getters and setters
    def get_folder(self):
        return self.folder

    def get_database(self):
        return self.database

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

    def set_ext(self, new):
        self.ext = new

    def set_user(self, new):
        self.user = new

    def set_password(self, new):
        self.password = new

    def gen_file_name_from_obj(self, obj):
        """
            From an object, generate a file name (based on the type of the object and it's name) for saving / managing
            :param obj : the object from which generate the name
        """
        return re.sub(r"'(?P<name>[\w]*)'", r"\g<name>" + "_{}{}".format(obj.get_name(), self.ext), type(obj))

    @staticmethod
    def gen_table_name_from_obj(obj):
        """
            From an object, generate the associated table name
            :param obj : the object from which generate the name
        """
        return re.sub(r"'(?P<name>[\w]*)'", r"\g<name>", type(obj))

    def file_save(self, obj):
        """
            Save an object (Serialize) into a file (name given with gen_file_name_from_obj()
            :param obj : the object to save
        """
        with open(self.folder + self.gen_file_name_from_obj(obj), "wb") as f:
            pickle.dump(obj, f)

    def file_load(self, file_name):
        """
            From a file name, load the associated object and returns it
            :param file_name : the name of the file to load
            :return: the object loaded
        """
        with open(self.folder + file_name, "rb") as f:
            return pickle.load(f)

    def files_load(self):
        """
            Load all the objects from the dest directory into a dict and returns it
            :return: objs : the dictionary containing the objects loaded
        """
        objs = dict()
        for file in os.listdir(self.folder):
            with open(self.folder + file, "rb") as f:
                obj = pickle.load(f)
                objs[file] = obj
        return objs

    def init_db(self):
        """
            Creates all tables for the database to store ingredients, recipes ect...
        """
        connector = self.get_connector()
        cursor = connector.cursor()
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
            "deleted INT(1) DEFAULT 0, CONSTRAINT ShoppingList_PK PRIMARY KEY (id_shoppinglist)) ENGINE=InnoDB"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Purchase ( id_shoppinglist INT NOT NULL, id_ingredient Int NOT NULL, "
            "quantity INT NOT NULL, deleted INT(1) DEFAULT 0, CONSTRAINT Purchase_PK PRIMARY KEY (id_shoppinglist, id_ingredient), "
            "CONSTRAINT Purchase_Ingredient_FK FOREIGN KEY (id_ingredient) REFERENCES Ingredient(id_ingredient), "
            "CONSTRAINT Purchase_ShoppingList0_FK FOREIGN KEY (id_shoppinglist) REFERENCES ShoppingList(id_shoppinglist)) ENGINE=InnoDB"
        )
        connector.close()

    def get_connector(self):

        """
            Returns a mariadb connector to execute queries
            :return: connector : the mariadb cursor
        """
        try:
            config = {
                        'user': self.user,
                        'password': self.password,
                        'host': self.host,
                        'database': self.database,
                        'raise_on_warnings': True
                        }
            connector = mariadb.connect(**config)
        except mariadb.errors.ProgrammingError:
            print("Impossible to connect to the database.\nThe identifiers might not be correct :\nuser : {}"
                  "\npassword : {}\ndatabase : {}".format(self.user, self.password, self.database))
            quit(1)
        return connector

    def db_loads(self):
        """
        Loads all the elements from the database
        :return: The elements from database if exist else None
        """
        connect = self.get_connector()
        cursor = connect.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `{}` WHERE deleted = 0".format(self.table))
        answ = cursor.fetchall()
        connect.close()
        return answ if answ else None

    def get_db_fields(self):
        """
        Returns a list of the database's fields
        :return: answ : The list of fields in the own database
        """
        connect = self.get_connector()
        cursor = connect.cursor()
        cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='{}' AND `TABLE_NAME`='{}'".format(self.database, self.table))
        answ = cursor.fetchall()
        connect.close()
        return answ

    def get_field(self, field, id):
        """
        Returns the value of a selected field for a given id
        :param field: The field you want to get
        :param id: The id of the item you want to get the field
        :return: answ[0][0] : The value of the field
        """
        connect = self.get_connector()
        cursor = connect.cursor()
        cursor.execute("SELECT `{}` FROM `{}` WHERE deleted = 0 AND `id_{}` = {}".format(field, self.table,
                                                                                         self.table.lower(), id))
        answ = cursor.fetchall()
        connect.close()
        return answ[0][0]

    def set_field(self, id, field, value):
        """
        Set the value of a simple field given in parameter to a specific entry (given by it's id)
        :param id : The id of the entry to set
        :param field: The field to set
        :param value: The value to affect to the selected field
        :return: None
        """
        connect = self.get_connector()
        cursor = connect.cursor()
        cursor.execute('UPDATE `{}` SET `{}` = "{}" WHERE `id_{}` = {}'.format(self.table, field, value, self.table.lower(), id))
        connect.commit()
        connect.close()

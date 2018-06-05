from Controllers.IngredientManager import IngredientManager
from Controllers.Manager import Manager
import mysql.connector as mariadb

m = Manager("t", usr="jcoley", psswd="ttittaten7tretypolog")
m.init_db()


i = IngredientManager(usr="jcoley", psswd="ttittaten7tretypolog")
#i.db_create("aaa")
ing = i.db_load(15)
ing.describe()
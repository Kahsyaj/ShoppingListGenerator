from Controllers.IngredientManager import IngredientManager
from Controllers.PurchaseManager import PurchaseManager
from Controllers.Manager import Manager
# pip install mariadb
# pip install pymysql
import mysql.connector as mariadb

m = Manager("t", usr="jcoley", psswd="ttittaten7tretypolog")
m.init_db()


i = IngredientManager(usr="jcoley", psswd="ttittaten7tretypolog")
p = PurchaseManager(usr="jcoley", psswd="ttittaten7tretypolog")
#i.db_create("aaa")
ing = i.db_load(15)
ing.describe()
pur = p.db_load(1)
pur.describe()
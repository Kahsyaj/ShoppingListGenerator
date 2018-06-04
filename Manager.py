################################################################################
# Manager class which deals with objects saving / loading / setting / deleting #
################################################################################
import pickle
import re
import os


class Manager:
    # dest represent the output destination such as file or database
    def __init__(self, mode="file"):
        self.mode = mode
        if mode == "file":
            self.dest = "../ShpLstSave/"
            self.ext = ".bak"
        elif mode == "database":
            self.dest = "ShoppingList"
            self.tbls = []
        else:
            raise ValueError('You can only choose between "file" and "database".')

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

    def gen_file_name_from_obj(self, obj):
        return re.sub(r"'(?P<name>[\w]*)'", r"\g<name>" + self.ext, type(obj))

    def file_save(self, obj):
        with open(self.gen_file_name_from_obj(obj), "ab") as file:
            pickle.dump(obj, file)

    def files_load(self):
        objs = dict()
        for file in os.listdir(self.dest):
            with open(self.dest + file, "rb") as f:
                obj = pickle.load(f)
                objs[file] = obj
        return objs


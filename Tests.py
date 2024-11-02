import synced_database
import os


class Tests:
    FILE_PATH = 'TEST'

    def __init__(self, test_dict, num_of):
        self.test_dict = test_dict
        self.num_of = num_of

    def create_file(self, file_path):
        # create file w test_dict
        db = synced_database.SyncedDatabase(file_path, 'mode')
        return db.dict_set(self.test_dict)

    def delete_file(self, file_path):
        # delete file
        if os.path.exists(self, file_path):
            os.remove(file_path)

    @staticmethod
    def write_read(db, key, val):
        # write and read to see if worked
        db.value_set(key, val)
        value = db.value_get(key)
        return value == val

    @staticmethod
    def delete_read(db, key):
        # delete and read to see if worked
        db.value_delete(key)
        return key in dict.keys()

    def read_mult(self, func):
        # read multi=num_of
        counter = 0
        while counter != self.num_of:
            func()
            counter = counter + 1

    # def run_all(self, func):
        # run all
# ASSERTS:
#         if os.path.exists(self.file_path):
#             return False
#         return True

import threading
import time

import synced_database
import os


class Tests:

    def __init__(self, test_dict, mode):
        self.test_dict = test_dict
        self.mode = mode

    #@staticmethod
    def func(self, f5, arg):
        print("func")

    def locki(self, thing):
        if self.mode == 'threads':
            if isinstance(thing, threading.Semaphore):
                v = not thing.acquire(blocking=False)
                if not v:
                    thing.release()
            else:
                v = thing.locked()

        elif self.mode == 'processes':
            v = not thing.acquire(block=False)
            if not v:
                thing.release()
        else:
            v = 'err'
        return v

    def create_file(self, file_path):
        # create file w test_dict
        db = synced_database.SyncedDatabase(file_path, self.mode)
        print(db.dict_set(self.test_dict))
        return db

    @staticmethod
    def delete_file(file_path):
        # delete file
        if os.path.exists(file_path):
            os.remove(file_path)
        print(not os.path.exists(file_path))

    def check_multread_write(self, sdb, key, val):
        things = []
        count = 0
        valu = True
        while count < sdb.max:
            count = count + 1
            if self.locki(sdb.read_semaphore) or sdb.get_val_of_sem() >= sdb.max:
                valu = False
            thing = self.func(sdb.value_get, [key])
            things.append(thing)
        v = sdb.value_set(key, val)
        print(valu)
        return things

    def check_multread(self, sdb, key):
        things = []
        count = 0
        val = True
        while count < sdb.max:
            count = count+1
            if self.locki(sdb.read_semaphore):
                val = False
            thing = self.func(sdb.value_get, [key])
            things.append(thing)
        print(val)
        return things

    def read_no_write(self, sdb, key, val):
        value = False
        thing = self.func(sdb.value_get, [key])
        time.sleep(1)
        # if not self.locki(sdb.read_semaphore):
        #     while not self.locki(sdb.read_semaphore):
        #         continue
        if sdb.get_val_of_sem() < sdb.max:
            value = True
        print(value)
        return [thing]

    def write_no_read(self, sdb, key, val):
        value = False
        thing = self.func(sdb.value_set, [key, val])
        time.sleep(1)
        if self.locki(sdb.read_semaphore):
            value = True
        print(value)
        return [thing]

    # @staticmethod
    def write_per(self, sdb, key, val):
        # write wo comp & read wo comp
        value = False
        if not self.locki(sdb.write_lock):
            if sdb.value_set(key, val) and val == sdb.value_get(key):
                if not self.locki(sdb.write_lock):
                    value = True
        return value

    def read_per(self, sdb, key, val):
        # write wo comp & read wo comp
        value = False
        sdb.value_set(key, val)
        if not self.locki(sdb.read_lock):
            if val == sdb.value_get(key):
                if not self.locki(sdb.read_lock):
                    value = True
        return value

    @staticmethod
    def delete_read(sdb, key):
        # delete wo comp
        val = sdb.value_get(key)
        val2 = sdb.value_delete(key)
        return key not in sdb.dict_keys() and val == val2

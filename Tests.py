"""
Bar Assulin
Tests
"""

import threading
import time
import synced_database
import os


class Tests:
    """
    A class for testing concurrent read/write operations on a synchronized database.
    
    Attributes:
    - test_dict: Dictionary of initial data to load into the database.
    - mode: Specifies 'threads' or 'processes' to determine locking mechanism.
    """

    def __init__(self, test_dict, mode):
        """
        Initializes the test object with a dictionary and mode (threads/processes).
        
        Parameters:
        - test_dict: Dictionary of initial key-value pairs for database setup.
        - mode: Specifies mode, either 'threads' or 'processes'.
        """
        self.test_dict = test_dict
        self.mode = mode

    def func(self, f5, arg):
        """
        Starts a function in a new thread/process.
        
        Parameters:
        - f5: Function to be executed.
        - arg: Arguments to pass to the function.
        
        Returns:
        - A new thread or process executing the function with the given arguments.
        """
        print("func")

    def locki(self, thing):
        """
        Checks the lock status of the given semaphore/lock.
        
        Parameters:
        - thing: Semaphore or lock to check.
        
        Returns:
        - Boolean indicating lock status (True if locked, False if free).
        """
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
        """
        Creates a new database file with initial test data.
        
        Parameters:
        - file_path: Path for the database file.
        
        Returns:
        - SyncedDatabase object initialized with test data.
        """
        db = synced_database.SyncedDatabase(file_path, self.mode)
        print(db.dict_set(self.test_dict))
        return db

    @staticmethod
    def delete_file(file_path):
        """
        Deletes the specified database file.
        
        Parameters:
        - file_path: Path of the file to delete.
        
        Prints:
        - Whether the file was successfully deleted.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        print(not os.path.exists(file_path))

    def check_multread_write(self, sdb, key, val):
        """
        Checks multiple readers with a writer.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to read/write.
        - val: Value to write.
        
        Returns:
        - List of reader threads/processes created.
        """
        things = []
        count = 0
        valu = True
        while count < sdb.max:
            count = count + 1
            if self.locki(sdb.read_semaphore):
                valu = False
            thing = self.func(sdb.value_get, [key])
            things.append(thing)
        v = sdb.value_set(key, val)
        print(valu)
        return things

    def check_multread(self, sdb, key):
        """
        Checks multiple concurrent readers.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to read.
        
        Returns:
        - List of reader threads/processes created.
        """
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
        """
        Reads while ensuring no write operations are active.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to read.
        - val: Expected value to confirm reading.
        
        Returns:
        - List containing the reader thread/process.
        """
        value = False
        thing = self.func(sdb.value_get, [key])
        time.sleep(1)
        if sdb.get_val_of_sem() < sdb.max:
            value = True
        print(value)
        return [thing]

    def write_no_read(self, sdb, key, val):
        """
        Writes while ensuring no read operations are active.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to write.
        - val: Value to write.
        
        Returns:
        - List containing the writer thread/process.
        """
        value = False
        thing = self.func(sdb.value_set, [key, val])
        time.sleep(1)
        if self.locki(sdb.read_semaphore):
            value = True
        print(value)
        return [thing]

    def write_per(self, sdb, key, val):
        """
        Performs a write operation while ensuring no concurrent writes.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to write.
        - val: Value to write.
        
        Returns:
        - Boolean indicating success of write operation without contention.
        """
        value = False
        if not self.locki(sdb.write_lock):
            if sdb.value_set(key, val) and val == sdb.value_get(key):
                if not self.locki(sdb.write_lock):
                    value = True
        return value

    def read_per(self, sdb, key, val):
        """
        Performs a read operation while ensuring no concurrent reads.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to read.
        - val: Expected value to confirm reading.
        
        Returns:
        - Boolean indicating success of read operation without contention.
        """
        value = False
        sdb.value_set(key, val)
        if not self.locki(sdb.read_lock):
            if val == sdb.value_get(key):
                if not self.locki(sdb.read_lock):
                    value = True
        return value

    @staticmethod
    def delete_read(sdb, key):
        """
        Deletes a value and verifies deletion by reading.
        
        Parameters:
        - sdb: SyncedDatabase object.
        - key: Key to delete.
        
        Returns:
        - Boolean indicating success of delete-read consistency.
        """
        val = sdb.value_get(key)
        val2 = sdb.value_delete(key)
        return key not in sdb.dict_keys() and val == val2

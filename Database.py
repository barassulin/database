"""
Bar Asullin
data to file
"""

from SimpleDatabase import SimpleDatabase
import os
import pickle


class Database(SimpleDatabase):
    def __init__(self, file_path):
        """
        Initializes the Database with a specified file path for persistence.

        Parameters:
        - file_path: Path to the file used to save/load the database.

        The constructor sets the file path and calls the superclass initializer
        to set up the in-memory database structure.
        """
        self.file_path = file_path
        super().__init__()

    def _load_database(self):
        """
        Loads the database from the specified file if it exists.

        This method checks if the file exists. If it does, it opens the file in binary
        read mode ('rb') and loads the data into the in-memory database (self.db) using pickle.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                self.db = pickle.load(f)

    def _save_database(self):
        """
        Saves the current in-memory database to the file.

        If the file exists, it overwrites it in binary write mode ('wb'). If the file does
        not exist, it creates the file in append binary mode ('ab') before saving. The data
        is serialized using pickle.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'wb') as f:
                pickle.dump(self.db, f)
        else:
            with open(self.file_path, 'ab') as f:
                pickle.dump(self.db, f)

    def value_set(self, key, val):
        """
        Adds a key-value pair to the database and saves the change to the file.

        Parameters:
        - key: The key under which the value is stored.
        - val: The value to store in the database.

        Returns:
        - True if the operation succeeded and was saved; False otherwise.

        This method first calls the superclass's value_set method to set the value.
        If successful, it then saves the database to the file.
        """
        success = super().value_set(key, val)
        if success:
            self._save_database()
        return success

    def dict_set(self, dict):
        """
        Updates the database with key-value pairs from a given dictionary and saves to the file.

        Parameters:
        - dict: A dictionary containing key-value pairs to add to the database.

        Returns:
        - True if the operation succeeded and was saved; False otherwise.

        This method calls the superclass's dict_set method to update the database with
        the dictionary. If successful, it saves the change to the file.
        """
        success = super().dict_set(dict)
        if success:
            self._save_database()
        return success

    def dict_keys(self):
        """
        Returns a view of the keys currently stored in the database.

        Returns:
        - A view object displaying all keys in the database.

        This method calls the superclass's dict_keys method to retrieve a view of the keys
        in the in-memory database. This method does not modify the file.
        """
        result = super().dict_keys()
        return result

    def value_delete(self, key):
        """
        Deletes a key-value pair from the database and saves the change to the file.

        Parameters:
        - key: The key to delete from the database.

        Returns:
        - The value that was deleted if the key existed; None if the key was not found.

        This method calls the superclass's value_delete method to remove the key-value pair.
        If the deletion was successful, it saves the updated database to the file.
        """
        val = super().value_delete(key)
        if val is not None:
            self._save_database()
        return val

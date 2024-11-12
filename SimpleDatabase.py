"""
Bar Assulin
database of dict
"""

class SimpleDatabase:
    def __init__(self):
        self.db = {}  # Initialize an empty dictionary to act as the database

    def value_set(self, key, val):
        """
        Adds the value 'val' with the key 'key' to the database.

        Parameters:
        - key: The key associated with the value in the database.
        - val: The value to store in the database.

        Returns:
        - True if the operation succeeded, False otherwise.
        """
        try:
            self.db[key] = val  # Attempt to add/update the key-value pair
            r = True
        except Exception as err:
            print(err)  # Print error if any exception occurs
            r = False
        finally:
            return r

    def value_get(self, key):
        """
        Retrieves the value associated with the key 'key', or returns None if not found.

        Parameters:
        - key: The key whose associated value is to be returned.

        Returns:
        - The value associated with the key, or None if the key is not found.
        """
        try:
            r = self.db.get(key)  # Use .get() to safely retrieve the value
        except Exception as err:
            print(err)  # Print error if any exception occurs
            r = None
        finally:
            return r

    def value_delete(self, key):
        """
        Deletes the value associated with the key 'key' and returns it, or None if the key is not found.

        Parameters:
        - key: The key whose associated value is to be deleted.

        Returns:
        - The deleted value, or None if the key was not in the database.
        """
        try:
            r = self.db.pop(key)  # Remove the key-value pair and return the value
        except KeyError:
            print(f"Key '{key}' not found in the database.")  # Handle missing key error
            r = None
        except Exception as err:
            print(err)  # Print error if any other exception occurs
            r = None
        finally:
            return r

    def dict_set(self, new_dict):
        """
        Updates the database with the key-value pairs from the provided dictionary.

        Parameters:
        - new_dict: A dictionary to merge into the existing database.

        Returns:
        - True if the operation succeeded, False otherwise.
        """
        try:
            self.db.update(new_dict)  # Update the database with key-value pairs from new_dict
            r = True
        except Exception as err:
            print(err)  # Print error if any exception occurs
            r = False
        finally:
            return r

    def dict_keys(self):
        """
        Returns a view object of the database's keys.

        Returns:
        - A view object that displays a list of all keys in the database.
        """
        return self.db.keys()  # Return all keys in the database as a view object

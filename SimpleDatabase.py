
class SimpleDatabase:
    def __init__(self):
        self.db = {}  # אובייקט dict עבור ה-database

    def value_set(self, key, val):
        """מוסיף את הערך 'val' עם המפתח 'key' ל-dict"""
        self.db[key] = val
        return True  # הצלחה

    def value_get(self, key):
        """מחזיר את הערך שמותאם למפתח 'key', או None אם לא קיים"""
        return self.db.get(key, None)

    def value_delete(self, key):
        """מוחק את הערך שמתאים למפתח 'key' ומחזיר אותו, או None אם לא קיים"""
        return self.db.pop(key, None)

    def dict_set(self, dict):
        """add dict to the db dict"""
        self.db.update(dict)

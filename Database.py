import SimpleDatabase
import os
import pickle

class Database(SimpleDatabase):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self._load_database()  # טוען נתונים מהקובץ, אם קיים

    def _load_database(self):
        """טוען את ה-Database מתוך הקובץ"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                self.db = pickle.load(f)


    def _save_database(self):
        """שומר את ה-Database לקובץ"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'wb') as f:
                pickle.dump(self.db, f)
        else:
            with open(self.file_path, 'ab') as f:
                pickle.dump(self.db, f)

    def value_set(self, key, val):
        """מוסיף את הערך עם המפתח ושומר את השינוי בקובץ"""
        success = super().value_set(key, val)
        if success:
            self._save_database()
        return success

    def dict_set(self, dict):
        """מוסיף את הערך עם המפתח ושומר את השינוי בקובץ"""
        success = super().dict_set(dict)
        if success:
            self._save_database()
        return success

    def value_delete(self, key):
        """מוחק את הערך עם המפתח ושומר את השינוי בקובץ"""
        val = super().value_delete(key)
        if val is not None:
            self._save_database()
        return val

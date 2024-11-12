"""
Bar Assulin
Sync
"""

import time
from multiprocessing import Semaphore as ProcessSemaphore, Lock as ProcessLock
from threading import Semaphore as ThreadSemaphore, Lock as ThreadLock
from Database import Database


class SyncedDatabase(Database):
    """
    A database class with synchronization mechanisms for either threads or processes.
    The class ensures that concurrent access to the database is properly managed using locks and semaphores.

    Attributes:
        max (int): The maximum number of concurrent readers allowed.
        mode (str): The synchronization mode, either 'threads' or 'processes'.
        read_lock (Lock): A lock to ensure mutual exclusion for read operations.
        write_lock (Lock): A lock to ensure mutual exclusion for write operations.
        read_semaphore (Semaphore): A semaphore to limit the number of concurrent readers.
    """

    def __init__(self, file_path, mode):
        """
        Initializes the SyncedDatabase with the specified file path and synchronization mode.

        Args:
            file_path (str): The file path to initialize the database with.
            mode (str): The mode of synchronization ('threads' or 'processes').

        Raises:
            ValueError: If the mode is not 'threads' or 'processes'.
        """
        super().__init__(file_path)
        self.max = 10  # Maximum number of concurrent readers
        self.mode = mode

        # Select synchronization objects based on the mode
        if mode == 'threads':
            self.read_lock = ThreadLock()  # Lock for read operations
            self.write_lock = ThreadLock()  # Lock for write operations
            self.read_semaphore = ThreadSemaphore(self.max)  # Semaphore to limit concurrent readers
        elif mode == 'processes':
            self.read_lock = ProcessLock()  # Lock for read operations
            self.write_lock = ProcessLock()  # Lock for write operations
            self.read_semaphore = ProcessSemaphore(self.max)  # Semaphore to limit concurrent readers
        else:
            raise ValueError("Mode must be either 'threads' or 'processes'")

    def get_val_of_sem(self):
        """
        Retrieves the current value of the read semaphore.

        Returns:
            int: The current value of the read semaphore, indicating the number of available reader slots.
        """
        if self.mode == 'threads':
            val = self.read_semaphore._value
        else:
            val = self.read_semaphore.get_value()
        return val

    def acquire_read(self):
        """
        Acquires the read semaphore, allowing a read operation to proceed.

        Blocks if the maximum number of concurrent readers is reached, or if a writer is active.
        """
        self.read_semaphore.acquire()

    def release_read(self):
        """
        Releases the read semaphore, allowing other readers to proceed.

        This method should be called after completing a read operation.
        """
        self.read_semaphore.release()

    def acquire_write(self):
        """
        Acquires exclusive write access.

        This method blocks all readers and writers, ensuring that only one writer can access the database at a time.
        """
        self.write_lock.acquire()  # Acquire the write lock
        for i in range(self.max):  # Block all readers
            self.read_semaphore.acquire()

    def release_write(self):
        """
        Releases exclusive write access.

        This method should be called after completing a write operation.
        """
        self.write_lock.release()  # Release the write lock
        for i in range(self.max):  # Release all readers
            self.read_semaphore.release()

    def value_set(self, key, val):
        """
        Sets a value in the database with exclusive write access.

        Args:
            key: The key of the value to set.
            val: The value to be set.

        Returns:
            bool: True if the value was successfully set, False otherwise.
        """
        self.acquire_write()
        result = super().value_set(key, val)
        time.sleep(2)  # Simulate delay for write operation
        self.release_write()
        return result

    def dict_set(self, dict):
        """
        Sets multiple key-value pairs in the database with exclusive write access.

        Args:
            dict (dict): A dictionary of key-value pairs to set.

        Returns:
            bool: True if the dictionary was successfully set, False otherwise.
        """
        self.acquire_write()
        result = super().dict_set(dict)
        time.sleep(2)  # Simulate delay for write operation
        self.release_write()
        return result

    def dict_keys(self):
        """
        Retrieves all the keys from the database with shared read access.

        Returns:
            list: A list of all keys in the database.
        """
        self.acquire_read()
        result = super().dict_keys()
        time.sleep(2)  # Simulate delay for read operation
        self.release_read()
        return result

    def value_get(self, key):
        """
        Gets a value from the database with shared read access.

        Args:
            key: The key of the value to retrieve.

        Returns:
            The value associated with the specified key.
        """
        self.acquire_read()
        result = super().value_get(key)
        time.sleep(2)  # Simulate delay for read operation
        self.release_read()
        return result

    def value_delete(self, key):
        """
        Deletes a value from the database with exclusive write access.

        Args:
            key: The key of the value to delete.

        Returns:
            bool: True if the value was successfully deleted, False otherwise.
        """
        self.acquire_write()
        result = super().value_delete(key)
        time.sleep(2)  # Simulate delay for write operation
        self.release_write()
        return result

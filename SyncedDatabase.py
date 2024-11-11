import time
from multiprocessing import Semaphore as ProcessSemaphore, Lock as ProcessLock
from threading import Semaphore as ThreadSemaphore, Lock as ThreadLock
from Database import Database


class SyncedDatabase(Database):
    def __init__(self, file_path, mode):
        super().__init__(file_path)
        self.max = 10
        self.mode = mode

        # Select synchronization objects based on mode
        if mode == 'threads':
            self.read_lock = ThreadLock()
            self.write_lock = ThreadLock()
            self.read_semaphore = ThreadSemaphore(self.max)  # Max 10 concurrent readers
        elif mode == 'processes':
            self.read_lock = ProcessLock()
            self.write_lock = ProcessLock()
            self.read_semaphore = ProcessSemaphore(self.max)
        else:
            raise ValueError("Mode must be either 'threads' or 'processes'")

    def get_val_of_sem(self):
        if self.mode == 'threads':
            val = self.read_semaphore._value
        else:
            val = self.read_semaphore.get_value()
        return val

    def acquire_read(self):
        """Allow up to 10 concurrent readers, but block if writer is active."""
        self.read_semaphore.acquire()

    def release_read(self):
        """Release read lock and update reader count."""
        self.read_semaphore.release()

    def acquire_write(self):
        """Acquire exclusive write access."""
        self.write_lock.acquire()
        for i in range(self.max):
            self.read_semaphore.acquire()

    def release_write(self):
        """Release exclusive write access."""
        self.write_lock.release()
        for i in range(self.max):
            self.read_semaphore.release()

    def value_set(self, key, val):
        """Set value with exclusive write access."""
        self.acquire_write()
        result = super().value_set(key, val)
        time.sleep(2)
        self.release_write()
        return result

    def dict_set(self, dict):
        # private?
        """Set value with exclusive write access."""
        self.acquire_write()
        result = super().dict_set(dict)
        time.sleep(2)
        self.release_write()
        return result

    def dict_keys(self):
        # private?
        """Set value with exclusive write access."""
        self.acquire_read()
        result = super().dict_keys()
        time.sleep(2)
        self.release_read()
        return result

    def value_get(self, key):
        """Get value with shared read access."""
        self.acquire_read()
        result = super().value_get(key)
        time.sleep(2)
        self.release_read()
        return result

    def value_delete(self, key):
        """Delete value with exclusive write access."""
        self.acquire_write()
        result = super().value_delete(key)
        time.sleep(2)
        self.release_write()
        return result

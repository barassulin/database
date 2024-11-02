from multiprocessing import Lock as ProcessLock
from threading import Semaphore, Lock as ThreadLock
import Database


class SyncedDatabase(Database):
    def __init__(self, file_path, mode):
        super().__init__(file_path)

        # Select synchronization objects based on mode
        if mode == 'threads':
            self.read_lock = ThreadLock()
            self.write_lock = ThreadLock()
            self.read_semaphore = Semaphore(10)  # Max 10 concurrent readers
        elif mode == 'processes':
            self.read_lock = ProcessLock()
            self.write_lock = ProcessLock()
            self.read_semaphore = Semaphore(10)
        else:
            raise ValueError("Mode must be either 'threads' or 'processes'")

        self.read_count = 0

    def acquire_read(self):
        """Allow up to 10 concurrent readers, but block if writer is active."""
        self.read_semaphore.acquire()
        with self.read_lock:
            self.read_count += 1
            if self.read_count == 1:
                self.write_lock.acquire()

    def release_read(self):
        """Release read lock and update reader count."""
        with self.read_lock:
            self.read_count -= 1
            if self.read_count == 0:
                self.write_lock.release()
        self.read_semaphore.release()

    def acquire_write(self):
        """Acquire exclusive write access."""
        self.write_lock.acquire()

    def release_write(self):
        """Release exclusive write access."""
        self.write_lock.release()

    def value_set(self, key, val):
        """Set value with exclusive write access."""
        self.acquire_write()
        result = super().value_set(key, val)
        self.release_write()
        return result

    def dict_set(self, dict):
        #private?
        """Set value with exclusive write access."""
        self.acquire_write()
        result = super().dict_set(dict)
        self.release_write()
        return result

    def value_get(self, key):
        """Get value with shared read access."""
        self.acquire_read()
        result = super().value_get(key)
        self.release_read()
        return result

    def value_delete(self, key):
        """Delete value with exclusive write access."""
        self.acquire_write()
        result = super().value_delete(key)
        self.release_write()
        return result

"""
Bar Assulin
Test threads
"""

from threading import Thread
from Tests import Tests

# Constants
TEST_DICT = {
    1: 2,
    4: 5
}  # Initial test dictionary with key-value pairs to load into the database
FILE_PATH = 'TEST'  # Path for the test database file
KEY = 1  # Key to use in test operations
VAL = 4  # Value to use in test operations


def run(tt):
    """
    Executes a sequence of operations on the database to test concurrency and other behaviors.

    Parameters:
    - tt: An instance of the TestThreads class, which manages file operations and thread tests.

    This function performs multiple operations on the database, simulating concurrent read, write, 
    and delete actions and checking the behavior under these conditions. Each step outputs a number 
    to indicate its progress.
    """
    sdb = tt.create_file(FILE_PATH)  # Creates and returns a database object using the file path
    print("start")
    
    sdb.dict_set(TEST_DICT)  # Sets initial values from TEST_DICT in the database
    print("1")
    
    print(tt.write_per(sdb, KEY, VAL))  # Attempts to write a value and returns success or failure
    print("2")
    
    print(tt.delete_read(sdb, KEY))  # Attempts to delete and then read the value associated with KEY
    print("3")
    
    thread = tt.read_no_write(sdb, KEY, VAL)  # Starts a read operation without write interference
    thread[0].join()  # Waits for the read thread to complete
    print("4")
    
    thread = tt.write_no_read(sdb, KEY, VAL)  # Starts a write operation without read interference
    thread[0].join()  # Waits for the write thread to complete
    print("5")
    
    thread = tt.check_multread(sdb, KEY)  # Starts multiple concurrent read operations
    thread[0].join()  # Waits for one of the read threads to complete
    print("6")
    
    thread = tt.check_multread_write(sdb, KEY, VAL)  # Starts concurrent read and write operations
    thread[0].join()  # Waits for one thread to complete
    print("7")
    
    print(tt.read_per(sdb, KEY, VAL))  # Attempts to perform a read with periodic updates
    print("8")
    
    tt.delete_file(FILE_PATH)  # Deletes the test database file
    print('finish')


class TestThreads(Tests):
    def __init__(self, test_dict):
        """
        Initializes the TestThreads class with test data and a specific mode.

        Parameters:
        - test_dict: Dictionary containing initial test data for database operations.
        
        This subclass inherits from Tests and is configured to run in 'threads' mode.
        """
        super().__init__(test_dict, 'threads')

    def func(self, f5, arg):
        """
        Starts a new thread to execute a function with provided arguments.

        Parameters:
        - f5: The target function to run in a new thread.
        - arg: A tuple of arguments to pass to the target function.
        
        Returns:
        - The created and started thread.
        
        This method starts a separate thread, useful for testing concurrent operations on the database.
        """
        thread = Thread(target=f5, args=arg)
        thread.start()
        return thread


if __name__ == "__main__":
    tt = TestThreads(TEST_DICT)  # Initializes the test class with the test dictionary
    run(tt)  # Executes the run function with the test class instance

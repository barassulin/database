"""
Bar Assulin
Test processes
"""
from multiprocessing import Process
from Tests import Tests

# Constants
TEST_DICT = {
    1: 2,
    4: 5
}  # Initial test dictionary with key-value pairs to load into the database
FILE_PATH = 'TEST'  # Path for the test database file
KEY = 1  # Key to use in test operations
VAL = 4  # Value to use in test operations


def run(tp):
    """
    Executes a sequence of operations on the database to test concurrent processes and database behaviors.

    Parameters:
    - tp: An instance of the TestProcess class, which manages file operations and process-based tests.

    This function performs multiple operations on the database, simulating concurrent read, write,
    and delete actions across multiple processes, and checking the behavior under these conditions.
    Each step outputs a number to indicate its progress.
    """
    sdb = tp.create_file(FILE_PATH)  # Creates and returns a database object using the file path
    print("start")

    sdb.dict_set(TEST_DICT)  # Sets initial values from TEST_DICT in the database
    print("1")

    print(tp.write_per(sdb, KEY, VAL))  # Attempts to write a value and returns success or failure
    print("2")

    print(tp.delete_read(sdb, KEY))  # Attempts to delete and then read the value associated with KEY
    print("3")

    process = tp.read_no_write(sdb, KEY, VAL)  # Starts a read operation without write interference
    process[0].join()  # Waits for the read process to complete
    print("4")

    process = tp.write_no_read(sdb, KEY, VAL)  # Starts a write operation without read interference
    process[0].join()  # Waits for the write process to complete
    print("5")

    process = tp.check_multread(sdb, KEY)  # Starts multiple concurrent read operations
    process[0].join()  # Waits for one of the read processes to complete
    print("6")

    process = tp.check_multread_write(sdb, KEY, VAL)  # Starts concurrent read and write operations
    process[0].join()  # Waits for one of the processes to complete
    print("7")

    print(tp.read_per(sdb, KEY, VAL))  # Attempts to perform a read with periodic updates
    print("8")

    tp.delete_file(FILE_PATH)  # Deletes the test database file
    print('finish')


class TestProcess(Tests):
    def __init__(self, test_dict):
        """
        Initializes the TestProcess class with test data and sets the test mode to 'processes'.

        Parameters:
        - test_dict: Dictionary containing initial test data for database operations.

        This subclass inherits from Tests and is configured to run in 'processes' mode,
        allowing concurrent testing with multiprocessing.
        """
        super().__init__(test_dict, 'processes')

    @staticmethod
    def func(f5, arg):
        """
        Starts a new process to execute a function with provided arguments.

        Parameters:
        - f5: The target function to run in a new process.
        - arg: A tuple of arguments to pass to the target function.

        Returns:
        - The created and started process.

        This method starts a separate process, which is useful for testing concurrent operations
        on the database in an environment where multiprocessing is required.
        """
        process = Process(target=f5, args=arg)
        process.start()
        return process


if __name__ == "__main__":
    tp = TestProcess(TEST_DICT)  # Initializes the test class with the test dictionary
    run(tp)  # Executes the run function with the test class instance

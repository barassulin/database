from threading import Thread
import random
import Tests
import socket
# constants
TEST_DICT = {}
NUM_OF_TESTS = 11
FILE_PATH = 'TEST'
KEY = ''
VAL = ''
global reading
reading = False


def read(sdb):
    sdb.acquire_read()
    while reading:
        print('')
        # reading or blocked?
    sdb.release_read()



def multread(sdb):
    global reading
    count = 0
    if count < NUM_OF_TESTS:
        reading = True
        func(read(), sdb)
        count = count+1
    while count < NUM_OF_TESTS:
        func(read(), sdb)
        count = count+1
    reading = False



def run(ts):
    """
    handle a connection
    :param ts:
    :return: None
    """
    sdb = ts.create_file(FILE_PATH)
    print(ts.write_read(sdb, KEY, VAL))
    print(ts.delete_read(sdb, KEY))
    print(multread(sdb))
    ts.delete_file(FILE_PATH)


def func(f, arg):
    thread = Thread(target=f,
                    args=(arg))
    thread.start()


"""
multyreads:
open socket
func multyreads(func)
"""


"""
func run all
"""

"""
waiting f client
thread for all tasks
"""


class TestThreads(Tests):
    def __init__(self, test_dict):
        super().__init__(test_dict, 'threads')

"""
    def read_mult(self, func):
        # read multi=num_of
        counter = 0
        while counter != self.__numof:
            func()
            counter = counter + 1
"""


if __name__ == "__main__":
    """
    open socket
    creat testthread
    creat thread sevrer
    run all tests
    """
    global reading
    ts = TestThreads(TEST_DICT)
    run(ts)


"""
global count clients
keep connect clients while num of clients<numof
client keeps reading while num of clients<numof

"""

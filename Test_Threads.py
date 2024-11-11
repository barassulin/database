from threading import Thread
from Tests import Tests

# constants
TEST_DICT = {
    1: 2,
    4: 5
}
FILE_PATH = 'TEST'
KEY = 1
VAL = 4


def run(tt):
    """
    handle a connection
    :param tt:
    :return: None
    """
    sdb = tt.create_file(FILE_PATH)
    print("start")
    sdb.dict_set(TEST_DICT)
    print("1")
    print(tt.write_per(sdb, KEY, VAL))
    print("2")
    print(tt.delete_read(sdb, KEY))
    print("3")
    thread = tt.read_no_write(sdb, KEY, VAL)
    thread[0].join()
    print("4")
    thread = tt.write_no_read(sdb, KEY, VAL)
    thread[0].join()
    print("5")
    thread = tt.check_multread(sdb, KEY)
    thread[0].join()
    print("6")
    thread = tt.check_multread_write(sdb, KEY, VAL)
    thread[0].join()
    print("7")
    print(tt.read_per(sdb, KEY, VAL))
    print("8")
    tt.delete_file(FILE_PATH)
    print('finish')


class TestThreads(Tests):
    def __init__(self, test_dict):
        super().__init__(test_dict, 'threads')

    # @staticmethod
    def func(self, f5, arg):
        thread = Thread(target=f5,
                        args=arg)
        thread.start()
        return thread


if __name__ == "__main__":
    tt = TestThreads(TEST_DICT)
    run(tt)

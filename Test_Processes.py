from multiprocessing import Process
from Tests import Tests
# constants
TEST_DICT = {
    1: 2,
    4: 5
}
FILE_PATH = 'TEST'
KEY = 1
VAL = 4


def run(tp):
    """
    handle a connection
    :param tp:
    :return: None
    """
    sdb = tp.create_file(FILE_PATH)
    print("start")
    sdb.dict_set(TEST_DICT)
    print("1")
    print(tp.write_per(sdb, KEY, VAL))
    print("2")
    print(tp.delete_read(sdb, KEY))
    print("3")
    process = tp.read_no_write(sdb, KEY, VAL)
    process[0].join()
    print("4")
    process = tp.write_no_read(sdb, KEY, VAL)
    process[0].join()
    print("5")
    process = tp.check_multread(sdb, KEY)
    process[0].join()
    print("6")
    process = tp.check_multread_write(sdb, KEY, VAL)
    process[0].join()
    print("7")
    print(tp.read_per(sdb, KEY, VAL))
    print("8")
    tp.delete_file(FILE_PATH)
    print('finish')


class TestProcess(Tests):
    def __init__(self, test_dict):

        super().__init__(test_dict, 'processes')

    @staticmethod
    def func(f5, arg):
        process = Process(target=f5,
                          args=arg)
        process.start()
        return process


if __name__ == "__main__":
    tp = TestProcess(TEST_DICT)
    run(tp)

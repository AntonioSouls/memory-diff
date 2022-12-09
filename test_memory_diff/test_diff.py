import unittest   # The test framework
from memory_diff.diff import Diff   # The class to test


class Test_TestIncrementDecrement(unittest.TestCase):

    def test_saving_diff(self):
        diff_object = Diff('/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/Matecat_New.tmx', '/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/Matecat_Old.tmx','/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/diff_file.tmx')
        diff_object.diff_function()
        return



if __name__ == '__main__':
    unittest.main()
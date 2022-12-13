import unittest   # The test framework
from memory_diff.diff import Diff   # The class to test


class Test_TestIncrementDecrement(unittest.TestCase):

    def test_saving_diff(self,file_new: str = '/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/Matecat_New.tmx', file_old:str ='/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/Matecat_Old.tmx', file_diff:str = '/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/diff_file.tmx'):
        diff_object = Diff(file_new,file_old, file_diff)
        diff_object.diff_function()
        return




if __name__ == '__main__':
    unittest.main()
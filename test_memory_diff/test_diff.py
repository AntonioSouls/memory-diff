import unittest   # The test framework
from memory_diff.diff import Diff   # The class to test

class Test_TestIncrementDecrement(unittest.TestCase):

    def test_saving_diff(self):
        diff_object = Diff(r'/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/file_prova/fileNew.txt', r'/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/file_prova/fileOld.txt')
        modified_file = diff_object.saving_diff()
        self.assertEqual(r'/mnt/c/Users/Antonio/Desktop/memory-diff/test_memory_diff/file_prova/fileNew.txt', modified_file)



if __name__ == '__main__':
    unittest.main()
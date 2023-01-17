import unittest   # The test framework
from memory_diff.dataset_diff import DatasetDiff   # The class to test
from memory_diff.diff import Diff
import psutil


class Test_TestIncrementDecrement(unittest.TestCase):

    def test_saving_diff(self,directory_new:str ='/home/antonio-lanza/dataset/2022.3.0/en__sw',directory_old:str='/home/antonio-lanza/dataset/2022.2.0/en__sw',directory_diff:str='/home/antonio-lanza/dataset/diff_folder',directory_stats:str='/home/antonio-lanza/dataset/stats'):
        dataset_diff_object = DatasetDiff(directory_new,directory_old,directory_diff,directory_stats)
        dataset_diff_object.starting_diff()
        return

    # def test_diff_on_singles_files(self,file_new:str = '/home/antonio-lanza/dataset/2022.3.0/en__sw/MyMemory.46e57154c706da58319f.en-US__sw-SZ.tmx',file_old:str = '/home/antonio-lanza/dataset/2022.2.0/en__sw/MyMemory.46e57154c706da58319f.en-US__sw-SZ.tmx',file_diff:str ='/home/antonio-lanza/dataset/file_diff.tmx'):
    #     diff_object = Diff(file_new,file_old,file_diff)
    #     diff_object.diff_function()
    #     return

if __name__ == '__main__':
    unittest.main()
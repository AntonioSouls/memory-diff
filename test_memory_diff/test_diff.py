import unittest   # The test framework
from memory_diff.dataset_diff import DatasetDiff   # The class to test
from memory_diff.diff import Diff


class Test_TestIncrementDecrement(unittest.TestCase):

    def test_saving_diff(self,directory_new:str ='/home/antonio/big_datasets/2022.3.0/en__it',directory_old:str='/home/antonio/big_datasets/2022.2.0/en__it',directory_diff:str='/home/antonio/big_datasets/diff_folder',directory_stats:str='/home/antonio/big_datasets/stats'):
        dataset_diff_object = DatasetDiff(directory_new,directory_old,directory_diff,directory_stats)
        dataset_diff_object.starting_diff_on_dataset()
        return

    # def test_diff_on_singles_files(self,file_new:str = '/home/antonio/dataset/2022.3.0/en__sw/Opus.CCMatrix.en__sw.tmx',file_old:str = '/home/antonio/dataset/2022.2.0/en__sw/Opus.CCMatrix.en__sw.tmx',file_diff:str ='/home/antonio/dataset/Opus.CCMatrix.en__sw.tmx'):
    #     diff_object = Diff(file_new,file_old,file_diff)
    #     diff_object.diff_open_files()
    #     return
    
    # def test_diff_on_singles_files(self,file_new:str = '/home/antonio/dataset/2022.3.0/en__sw/MyMemory.f6841844ded9600e7d54.en-US__sw-SZ.tmx',file_old:str = '/home/antonio/dataset/2022.2.0/en__sw/MyMemory.f6841844ded9600e7d54.en-US__sw-SZ.tmx',file_diff:str ='/home/antonio/dataset/MyMemory.f6841844ded9600e7d54.en-US__sw-SZ.tmx'):
    #     diff_object = Diff(file_new,file_old,file_diff)
    #     diff_object.diff_open_files()
    #     return

    # def test_diff_on_singles_files(self,file_new:str = '/home/antonio/dataset/2022.3.0/en__sw/Matecat.P24171J29476.en-US__sw-SZ.tmx',file_old:str = '/home/antonio/dataset/2022.2.0/en__sw/Matecat.P24171J29476.en-US__sw-SZ.tmx',file_diff:str ='/home/antonio/dataset/Matecat.P24171J29476.en-US__sw-SZ.tmx'):
    #     diff_object = Diff(file_new,file_old,file_diff)
    #     diff_object.diff_open_files()
    #     return

if __name__ == '__main__':
    unittest.main()
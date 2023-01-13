import unittest   # The test framework
from memory_diff.diff import Diff   # The class to test
from pathlib import Path
import shutil
from tqdm import tqdm

class Test_TestIncrementDecrement(unittest.TestCase):

    def test_saving_diff(self,file_new: str = '/home/antonio-lanza/dataset/2022.3.0/en__sw/Matecat.P60168J72993.en-GB__sw-SZ.tmx', file_old:str ='/home/antonio-lanza/dataset/2022.2.0/en__sw/Matecat.P60168J72993.en-GB__sw-SZ.tmx', file_diff:str = '/home/antonio-lanza/dataset/diff_file.tmx'):
        diff_object = Diff(file_new,file_old, file_diff)
        diff_object.diff_function()
        return


if __name__ == '__main__':
    unittest.main()
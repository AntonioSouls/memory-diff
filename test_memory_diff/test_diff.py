import unittest   # The test framework
from memory_diff.diff import Diff   # The class to test
import os
import filecmp


class Test_TestIncrementDecrement(unittest.TestCase):

    # def test_saving_diff(self,file_new: str = '/home/antonio-lanza/dataset/2022.3.0', file_old:str ='/home/antonio-lanza/dataset/2022.2.0', file_diff:str = '/home/antonio-lanza/dataset/diff_file.tmx'):
    #     diff_object = Diff(file_new,file_old, file_diff)
    #     diff_object.diff_function()
    #     return

    def test_diff_on_dataset(self,directory_new: str = '/home/antonio-lanza/dataset/2022.3.0/en__sw', directory_old: str = '/home/antonio-lanza/dataset/2022.2.0/en__sw', directory_diff:str = '/home/antonio-lanza/dataset/diff_folder'):
        os.chdir(directory_new)
        list_file_new = os.listdir()
        os.chdir(directory_old)
        list_file_old = os.listdir()
        for file_new in list_file_new:
            file_old = None
            for i in range(len(list_file_old)):
                if filecmp.cmp(file_new,list_file_old[i]):
                    file_old = list_file_old[i]
                    break
            os.chdir(directory_diff)
            file_diff = os.mkdir(file_new)
            if file_old == None:
                with open(file_new,'r') as file_object_new:
                    opened_file_new = file_object_new.read()
                with open(file_diff,'wb') as file_object_diff:
                    file_object_diff.writelines(opened_file_new)
            else:
                diff_object = Diff(file_new,file_old,file_diff)
                diff_object.diff_function()
        return


if __name__ == '__main__':
    unittest.main()
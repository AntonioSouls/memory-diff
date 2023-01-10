import unittest   # The test framework
from memory_diff.diff import Diff   # The class to test
from pathlib import Path
import shutil
from tqdm import tqdm

class Test_TestIncrementDecrement(unittest.TestCase):

    # def test_saving_diff(self,file_new: str = '/home/antonio-lanza/dataset/2022.3.0/en__sw/MyMemory.fca687d6379e9e8b7dd2.en-US__sw-SZ.tmx', file_old:str ='/home/antonio-lanza/dataset/2022.2.0/en__sw/MyMemory.fca687d6379e9e8b7dd2.en-US__sw-SZ.tmx', file_diff:str = '/home/antonio-lanza/dataset/diff_file.tmx'):
    #     diff_object = Diff(file_new,file_old, file_diff)
    #     diff_object.diff_function()
    #     return

    def test_diff_on_dataset(self,directory_new: str = '/home/antonio-lanza/dataset/2022.3.0/en__sw', directory_old: str = '/home/antonio-lanza/dataset/2022.2.0/en__sw', directory_diff:str = '/home/antonio-lanza/dataset/diff_folder'):
        directory_new_path = Path(directory_new)
        directory_old_path = Path(directory_old)
        list_file_new = list(directory_new_path.iterdir())
        list_file_old = list(directory_old_path.iterdir())
        old_names = [f.name for f in list_file_old]
        for file_new in tqdm(list_file_new):
            file_old = None
            diff_file = str(Path(directory_diff) / file_new.name)
            if file_new.name in old_names:
                file_old = list_file_old[old_names.index(file_new.name)]
                diff_object = Diff(str(file_new), str(file_old), diff_file)
                diff_object.diff_function()
            else:
                shutil.copyfile(file_new, diff_file)

        return


if __name__ == '__main__':
    unittest.main()
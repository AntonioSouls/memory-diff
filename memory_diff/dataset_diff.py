from pathlib import Path
import shutil
from tqdm import tqdm
from memory_diff.diff import Diff
import time
from numpy import mean

# Dataset_diff class that models an object that allows you to make the diff on entire dataset

class Dataset_diff:
    # CLASS CONSTRUCTOR: the object takes three directory as parameters, where the first one we insert is the dataset new's directory, the second one is the dataset old's directory
    # the third one is the directory in which we save all the files that contains only the differences
    def __init__(self,directory_new:str,directory_old:str,directory_diff:str) -> None:
        self.directory_new = directory_new
        self.directory_old = directory_old
        self.directory_diff = directory_diff
        self.total_diff_time = []

    # function that ciclate on entire dataset that contains a list of file new and the corresponding file old, so, that function, for each file_new, search the corresponding file old
    # (the file old with the same name) and invoke diff to make difference between those two files. This operation is made for all the file new in the dataset and the differences are saved into
    # the diff_folder
    def starting_diff(self):
        directory_new_path = Path(self.directory_new)
        directory_old_path = Path(self.directory_old)
        list_file_new = list(directory_new_path.iterdir())
        list_file_old = list(directory_old_path.iterdir())
        old_names = [f.name for f in list_file_old]
        for file_new in tqdm(list_file_new):
            if 'opus' not in file_new.name.lower() and file_new.name not in list(Path(self.directory_diff).iterdir()):  # I'm not considering the 'Opus' files because had problem to solve
                print(file_new)
                file_old = None
                diff_file = str(Path(self.directory_diff) / file_new.name)
                begin = time.time()
                if file_new.name in old_names:
                    file_old = list_file_old[old_names.index(file_new.name)]
                    print(file_old)
                    print(diff_file)
                    diff_object = Diff(str(file_new), str(file_old), diff_file)
                    diff_object.diff_function()
                else:
                    print(file_old)
                    print(diff_file)
                    shutil.copyfile(file_new, diff_file)
                ends = time.time()
                diff_time = ends - begin
                self.total_diff_time.append(diff_time)
                print(list_file_new.index(file_new))
                print('\n')
        self.print_stats()
        return
    

    def print_stats(self):
        directory_new_path_size = Path(self.directory_new).stat().st_size
        directory_old_path_size = Path(self.directory_old).stat().st_size
        directory_diff_path_size = Path(self.directory_diff).stat().st_size
        print('Dataset new size: ', directory_new_path_size, 'bytes', '\n')
        print('Dataset old size: ', directory_old_path_size, 'bytes', '\n')
        print('Dataset diff size: ', directory_diff_path_size, 'bytes', '\n')
        print('Average diff time: ', mean(self.total_diff_time), 'seconds','\n')
        print('Maximum diff time: ', max(self.total_diff_time), 'seconds', '\n')
        return
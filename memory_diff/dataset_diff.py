from pathlib import Path
import shutil
from tqdm import tqdm
from memory_diff.diff import Diff
import time
import psutil
from threading import Thread
from numpy import mean

# Dataset_diff class that models an object that allows you to make the diff on entire dataset

class DatasetDiff:
    # CLASS CONSTRUCTOR: the object takes three directory as parameters, where the first one we insert is the dataset new's directory, the second one is the dataset old's directory
    # the third one is the directory in which we save all the files that contains only the differences
    def __init__(self,directory_new:str,directory_old:str,directory_diff:str,directory_stats:str) -> None:
        self.directory_new = directory_new
        self.directory_old = directory_old
        self.directory_diff = directory_diff
        self.directory_stats = directory_stats
        self.total_diff_time = []


    # function that ciclate on entire dataset that contains a list of file new and the corresponding file old, so, that function, for each file_new, search the corresponding file old
    # (the file old with the same name) and invoke diff to make difference between those two files. This operation is made for all the file new in the dataset and the differences are saved into
    # the diff_folder
    def starting_diff(self):
        thread1 = Thread(target=self.cpu_usage)
        thread2 = Thread(target=self.ram_usage)
        thread1.start()
        thread2.start()
        directory_new_path = Path(self.directory_new)
        directory_old_path = Path(self.directory_old)
        list_file_new = list(directory_new_path.iterdir())
        list_file_old = list(directory_old_path.iterdir())
        old_names = [f.name for f in list_file_old]
        for file_new in tqdm(list_file_new):
            if 'opus' not in file_new.name.lower() and file_new.name not in list(Path(self.directory_diff).iterdir()):          # I'm not considering the 'Opus' files because had problem to solve
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
        thread1.join()
        thread2.join()
        self.print_stats()
        return
    

    # Function that print into a file all the diff's stats, so we can misure how much efficent our diff is
    def print_stats(self):
        file_stats = str(Path(self.directory_stats) / "final_stats.txt")
        directory_new_path_size = Path(self.directory_new).stat().st_size
        directory_old_path_size = Path(self.directory_old).stat().st_size
        directory_diff_path_size = Path(self.directory_diff).stat().st_size
        list_stats = []
        list_stats.append('Dataset new size: ' + str(directory_new_path_size) + ' bytes')
        list_stats.append('Dataset old size: ' + str(directory_old_path_size) + 'bytes')
        list_stats.append('Dataset diff size: ' + str(directory_diff_path_size) + 'bytes')
        list_stats.append('Average diff time: ' + str(mean(self.total_diff_time)) + 'seconds')
        list_stats.append('Maximum diff time: ' + str(max(self.total_diff_time)) + 'seconds')
        with open(file_stats, 'a+') as f:
            f.writelines(list_stats)
        return
    

    # Function that print into a file the CPU usage during the diff execution
    def cpu_usage(self):
        file_cpu_stats = str(Path(self.directory_stats) / "CPU_stats.txt")
        while(True):
            misuration_cpu_usage = str(psutil.cpu_percent())
            with open(file_cpu_stats, 'a+') as f:
                f.write('CPU usage: ' + misuration_cpu_usage+ "\n")
            time.sleep(10)
        return

    # Function that print into a file the RAM usage during the diff execution  
    def ram_usage(self):
        file_ram_stats = str(Path(self.directory_stats) / "RAM_stats.txt")
        while(True):
            misuration_ram_usage = str(psutil.virtual_memory()[2])
            with open(file_ram_stats, 'a+') as f:
                f.write('RAM usage: ' + misuration_ram_usage + "\n")
            time.sleep(10)
        return
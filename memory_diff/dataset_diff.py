from pathlib import Path
import shutil
from tqdm import tqdm
from memory_diff.diff import Diff
import time
import psutil
import logging
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
        self.total_CPU_usages = []
        self.total_RAM_usages = []
        self.total_execution_time = 0


    # function that ciclate on entire dataset that contains a list of file new and the corresponding file old, so, that function, for each file_new, search the corresponding file old
    # (the file old with the same name) and invoke diff to make difference between those two files. This operation is made for all the file new in the dataset and the differences are saved into
    # the diff_folder
    def starting_diff_on_dataset(self):
        logger = self.logging_func()
        thread1 = Thread(target=self.cpu_usage)
        thread2 = Thread(target=self.ram_usage)
        thread1.start()
        thread2.start()
        directory_new_path = Path(self.directory_new)
        directory_old_path = Path(self.directory_old)
        list_file_new = list(directory_new_path.iterdir())
        list_file_old = list(directory_old_path.iterdir())
        list_file_diff = list(Path(self.directory_diff).iterdir())
        old_names = [f.name for f in list_file_old]
        diff_names = [f.name for f in list_file_diff]
        start = time.time()
        for file_new in tqdm(list_file_new):
            if 'opus' not in file_new.name.lower() and file_new.name not in diff_names:          # I'm not considering the 'Opus' files because had problem to solve and not considering files that already contain the diff
                logger.info(f'{list_file_new.index(file_new)},{file_new.name}')
                file_old = None
                diff_file = str(Path(self.directory_diff) / file_new.name)
                begin = time.time()
                if file_new.name in old_names:
                    file_old = list_file_old[old_names.index(file_new.name)]
                    diff_object = Diff(str(file_new), str(file_old), diff_file)
                    diff_object.diff_open_files()
                else:
                    shutil.copyfile(file_new, diff_file)
                ends = time.time()
                diff_time = ends - begin
                self.total_diff_time.append(diff_time)
        stop = time.time()
        self.total_execution_time = stop - start
        self.print_stats()
        thread1.join()
        thread2.join()
    

    # Function that print into a file the logs of each file that Diff is parsing, so we can see (during the execution) wich file we're parsing
    def logging_func(self):
        file_log = str(Path(self.directory_stats) / "debug.log")
        logger = logging.getLogger('Diff_logger')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(file_log)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        formatter = logging.Formatter('%(asctime).19s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    
    # Function that print into a file all the diff's stats, so we can misure how much efficent our diff is
    def print_stats(self):
        file_stats = str(Path(self.directory_stats) / "final_stats.txt")
        directory_new_path_size = Path(self.directory_new).stat().st_size
        directory_old_path_size = Path(self.directory_old).stat().st_size
        directory_diff_path_size = Path(self.directory_diff).stat().st_size
        list_stats = []
        list_stats.append('Dataset new size: ' + str(directory_new_path_size) + ' bytes' + '\n')
        list_stats.append('Dataset old size: ' + str(directory_old_path_size) + 'bytes' + '\n')
        list_stats.append('Dataset diff size: ' + str(directory_diff_path_size) + 'bytes' + '\n')
        list_stats.append('Average diff time: ' + str(mean(self.total_diff_time)) + 'seconds' + '\n')
        list_stats.append('Maximum diff time: ' + str(max(self.total_diff_time)) + 'seconds' + '\n')
        list_stats.append('Total execution time: ' + str(self.total_execution_time) + 'seconds' + '\n')
        with open(file_stats, 'a+') as f:
            f.writelines(list_stats)
        
    

    # Function that print into a file the CPU usage during the diff execution
    def cpu_usage(self):
        file_cpu_stats = str(Path(self.directory_stats) / "CPU_stats.txt")
        while(True):
            misuration_cpu_usage = str(psutil.cpu_percent())
            with open(file_cpu_stats, 'a+') as f:
                f.write('CPU usage: ' + misuration_cpu_usage+ "\n")
                self.total_CPU_usages.append(misuration_cpu_usage)
            time.sleep(300)
        

    # Function that print into a file the RAM usage during the diff execution  
    def ram_usage(self):
        file_ram_stats = str(Path(self.directory_stats) / "RAM_stats.txt")
        while(True):
            misuration_ram_usage = str(psutil.virtual_memory()[2])
            with open(file_ram_stats, 'a+') as f:
                f.write('RAM usage: ' + misuration_ram_usage + "\n")
            self.total_RAM_usages.append(misuration_ram_usage)
            time.sleep(300)
from pathlib import Path
import shutil
from tqdm import tqdm
from memory_diff.diff import Diff
import time
import psutil
import logging
import threading
import multiprocessing
#from threading import Thread
from numpy import mean



class DatasetDiff:
    
    def __init__(self,directory_new:str,directory_old:str,directory_diff:str,directory_stats:str) -> None:
        self.directory_new = directory_new
        self.directory_old = directory_old
        self.directory_diff = directory_diff
        self.directory_stats = directory_stats
        self.total_diff_time = []
        self.total_CPU_usages = []
        self.total_RAM_usages = []
        self.total_execution_time = 0


   
    def starting_diff_on_dataset(self):
        logger = self.logging_func()
        event = threading.Event()
        thread1 = threading.Thread(target=self.cpu_usage,args=(event,))
        thread2 = threading.Thread(target=self.ram_usage,args=(event,))
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
            if file_new.name not in diff_names:         
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
        event.set()
        thread1.join()
        thread2.join()
    

    
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

    
   
    def print_stats(self):
        file_stats = str(Path(self.directory_stats) / "final_stats.txt")
        directory_new_path_size = 0
        directory_old_path_size = 0
        directory_diff_path_size = 0

        for file_new in Path(self.directory_new).iterdir():
            size = file_new.stat().st_size
            directory_new_path_size = directory_new_path_size + size

        for file_old in Path(self.directory_old).iterdir():
            size = file_old.stat().st_size
            directory_old_path_size = directory_old_path_size + size

        for file_diff in Path(self.directory_diff).iterdir():
            size = file_diff.stat().st_size
            directory_diff_path_size = directory_diff_path_size + size

        list_stats = []
        list_stats.append('Dataset new size: ' + str(directory_new_path_size) + ' bytes' + '\n')
        list_stats.append('Dataset old size: ' + str(directory_old_path_size) + 'bytes' + '\n')
        list_stats.append('Dataset diff size: ' + str(directory_diff_path_size) + 'bytes' + '\n')
        list_stats.append('\n')
        list_stats.append('Average CPU usage: ' + str(mean(self.total_CPU_usages)) + '%' + '\n')
        list_stats.append('Average RAM usage: ' + str(mean(self.total_RAM_usages)) + '%' + '\n')
        list_stats.append('\n')
        list_stats.append('Average diff time: ' + str(mean(self.total_diff_time)) + 'seconds' + '\n')
        list_stats.append('Maximum diff time: ' + str(max(self.total_diff_time)) + 'seconds' + '\n')
        list_stats.append('Total execution time: ' + str(self.total_execution_time) + 'seconds' + '\n')
        with open(file_stats, 'a+') as f:
            f.writelines(list_stats)
        
    

   
    def cpu_usage(self,event:threading.Event):
        print("Cpu Usage")
        file_cpu_stats = str(Path(self.directory_stats) / "CPU_stats.txt")
        while(not event.is_set()):
            misuration_cpu_usage = psutil.cpu_percent()
            with open(file_cpu_stats, 'a+') as f:
                f.write('CPU usage: ' + str(misuration_cpu_usage)+ "\n")
            self.total_CPU_usages.append(misuration_cpu_usage)
            time.sleep(300)
        

      
    def ram_usage(self,event:threading.Event):
        file_ram_stats = str(Path(self.directory_stats) / "RAM_stats.txt")
        while(not event.is_set()):
            misuration_ram_usage = psutil.virtual_memory()[2]
            with open(file_ram_stats, 'a+') as f:
                f.write('RAM usage: ' + str(misuration_ram_usage) + "\n")
            self.total_RAM_usages.append(misuration_ram_usage)
            time.sleep(300)
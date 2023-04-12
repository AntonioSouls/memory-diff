from pathlib import Path
from memory_diff.multiprocessing_utils import NoDeamonPool
import shutil
from tqdm import tqdm
from memory_diff.diff import Diff
import time
import psutil
import logging
import threading
import multiprocessing
import os
from numpy import mean


# DatasetDiff class that allows you to create an object that starts the Diff on the datasets to be compared.

class DatasetDiff:
    
    # It takes as parameters in order:
    #   - The path to the first dataset;
    #   - The path to the second dataset;
    #   - The dataset path where to save the Diff;
    #   - The path where to save the statistics;
    def __init__(self,directory_new:str,directory_old:str,directory_diff:str,directory_stats:str) -> None:
        self.directory_new = directory_new                             # Path specified
        self.directory_old = directory_old
        self.directory_diff = directory_diff
        self.directory_stats = directory_stats

        self.manager = multiprocessing.Manager()                       # Single manager to manage global variables
        
        self.total_diff_time = self.manager.list()                     # Variables useful for statistics
        self.total_CPU_usages = self.manager.list()
        self.total_RAM_usages = self.manager.list()
        self.total_execution_time = 0


    # Method to prepare the execution environment and start the diff
    def starting_diff_on_dataset(self):

        self.print_first_stats()

        logger = self.logging_func()                                      # I create a logger variable that I will use later to print the logging information to file
        
        event = threading.Event()                                         # I initiate an event that I will use to terminate the threads that will take care of printing the statistics of the CPU and RAM simultaneously with the execution of the code
        thread1 = threading.Thread(target=self.cpu_usage,args=(event,))   # I create the first Thread that will take care of printing the CPU statistics simultaneously with the execution of the code, specifying what is the function to execute to create the CPU statistics
        thread2 = threading.Thread(target=self.ram_usage,args=(event,))   # I create the first Thread that will take care of printing the RAM statistics simultaneously with the execution of the code, specifying what is the function to execute to create the RAM statistics
        thread1.start()                                                   # Starts first thread
        thread2.start()                                                   # Starts second thread
        
        directory_new_path = Path(self.directory_new)                      
        directory_old_path = Path(self.directory_old)
        list_file_new = self.manager.list(list(directory_new_path.iterdir()))           # I create a list containing all the files of the new dataset
        list_file_old = self.manager.list(list(directory_old_path.iterdir()))           # I create a list containing all the files of the old dataset
        list_file_diff = self.manager.list(list(Path(self.directory_diff).iterdir()))   # I create a list containing all the files of the dataset in which I wanna save the differences
        old_names = self.manager.list()                                                 # I create a list containing all the file names of the old dataset
        diff_names = self.manager.list()                                                # I create a list containing all the file names of the diff dataset
        old_names = [f.name for f in list_file_old]
        diff_names = [f.name for f in list_file_diff]

        pool = NoDeamonPool(8,)                                                        # I create a pool of 16 processes that will take care of making Diff on a file
        list_processes=list()                                                           # I need this to ensure that 16 files are analyzed at a time
        
        start = time.time()                                                             # I start a timer to calculate the start of the diff on the whole dataset, in order to measure how long it takes
        
        for file_new in tqdm(list_file_new):                                                                                                                                                         # For each file in the new dataset, I call the function to diff on that file 
            list_processes.append(pool.apply_async(DatasetDiff.file_selection,args=(file_new,diff_names,logger,list_file_new,old_names,list_file_old,self.total_diff_time,self.directory_diff)))     # I need this to make it happen in parallel to 16 files at a time
        pool.close()                                                                   # Deleting a process when it ends
        pool.join()                                                                    # I collect the result of the finished process

        stop = time.time()                                                             # I stopped the timer started at the beginning
        self.total_execution_time = stop - start                                       # Memorize the timer measurement
        self.print_stats()                                                             # I invoke the function which will print the statistics on the file within the specified directory
        event.set()                                                                    # I set the event to terminate the two threads I created
        thread1.join()                                                                 # I await the conclusion of both threads and collect the results
        thread2.join()
    

    # Method that starts the diff on the single file. See if the file we are analyzing is present in the old dataset. If present, invoke the class that does the diff within the file.
    # If not present, simply add the parsed file to dataset_diff. It also inputs the logger to log the single file to another logging file so you can
    # have debug information on an external file about each single file
    @staticmethod
    def file_selection(file_new:Path,diff_names:list,logger:logging,list_file_new:list,old_names:list,list_file_old:list,total_diff_time:list,directory_diff):
        if file_new.name not in diff_names:                                                    # I check that the new file is not already in the diff dataset because, if it already exists, it means that we have already analyzed it        
                logger.info(f'{list_file_new.index(file_new)},{file_new.name}')                # I save the logging information for the analyzed file on the external file
                file_old = None
                diff_file = str(Path(directory_diff) / file_new.name)
                begin = time.time()                                                            # I start a timer to calculate the start time of the diff on the single file, in order to know how long it takes the code to work on the single file
                if file_new.name in old_names:                                                 # If the analyzed file is also present in the old dataset, then I have to start the Diff class to make the differences at the file level
                    file_old = list_file_old[old_names.index(file_new.name)]
                    diff_object = Diff(str(file_new), str(file_old), diff_file)                # I create the Diff object which will do the diff on the file
                    diff_object.diff_open_files()                                              # I invoke the diff object method which will parse and save the differences between the two files
                    os.remove(file_old)
                else:                                                                          # If it is not present in the old dataset, then that file has been added, so it should be placed in the dataset_diff
                    shutil.copyfile(file_new, diff_file)
                os.remove(file_new)
                ends = time.time()                                                             # Stop the timer
                diff_time = ends - begin                                                       # I save the timer measurement in a list containing all diff time measurements
                total_diff_time.append(diff_time)
        return
    

    # Function to create the logger format and specify on which file to save the logging we do in the above function.
    # By running this function, we create a logger object which we then pass to the file_selection function so that, for each file, it uses this
    # logger object to save debug info for that file to an external file, inside the stats path
    def logging_func(self):
        file_log = str(Path(self.directory_stats) / "debug.log")                  # I specify that the file where to save the logging information is inside the path where to save the statistics
        logger = logging.getLogger('Diff_logger')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(file_log)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        formatter = logging.Formatter('%(asctime).19s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    # Method for saving statistics to a file. I print the size of the old and new datasets before starting with the diff because, during the execution, the Diff will erase all files into these two dataset 
    def print_first_stats(self):
        file_stats = str(Path(self.directory_stats) / "final_stats.txt")
        directory_new_path_size = 0
        directory_old_path_size = 0

        for file_new in Path(self.directory_new).iterdir():
            size = file_new.stat().st_size
            directory_new_path_size = directory_new_path_size + size

        for file_old in Path(self.directory_old).iterdir():
            size = file_old.stat().st_size
            directory_old_path_size = directory_old_path_size + size
        
        list_stats = []
        list_stats.append('Dataset new size (Before the Diff): ' + str(directory_new_path_size) + ' bytes' + '\n')
        list_stats.append('Dataset old size (Before the Diff): ' + str(directory_old_path_size) + 'bytes' + '\n')
        list_stats.append('\n')
        
        with open(file_stats, 'a+') as f:
            f.writelines(list_stats)
        return
    

   # Method for saving statistics to a file. I print the size of the diff datasets, Average use of RAM and CPU, Average execution time of the diff, maximum execution time of the diff
   # and code completion time. I do it after the diff's execution.
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
        list_stats.append('Dataset new size (After the Diff): ' + str(directory_new_path_size) + ' bytes' + '\n')
        list_stats.append('Dataset old size (After the Diff): ' + str(directory_old_path_size) + 'bytes' + '\n')
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
        
    

   # FUNCTIONS WHICH WILL BE LAUNCHED ON OTHER THREADS SO AS TO BE CARRIED OUT IN PARALLEL TO THE MAIN THREAD WHICH, INSTEAD, WILL CARRY OUT THE DIFF ON THE DATASET


   # Function to measure and print CPU utilization measurements to a file
    def cpu_usage(self,event:threading.Event):
        file_cpu_stats = str(Path(self.directory_stats) / "CPU_stats.txt")                         # I specify the path in which to save the file on which I will write all the measurements
        while(not event.is_set()):                                                                 # As long as the main-thread doesn't set the event, I keep printing the measurements to the file CPU
            misuration_cpu_usage = psutil.cpu_percent()
            with open(file_cpu_stats, 'a+') as f:
                f.write('CPU usage: ' + str(misuration_cpu_usage)+ "\n")
            self.total_CPU_usages.append(misuration_cpu_usage)
            time.sleep(300)                                                                        # I go to sleep for 5 minutes so that the stats are printed every 5 minutes and not repeatedly
        

    # Function to measure and print RAM usage measurements to a file
    def ram_usage(self,event:threading.Event):
        file_ram_stats = str(Path(self.directory_stats) / "RAM_stats.txt")                     # I specify the path in which to save the file on which I will write all the measurements
        while(not event.is_set()):                                                             # As long as the main-thread doesn't set the event, I keep printing the measurements to the file RAM
            misuration_ram_usage = psutil.virtual_memory()[2]
            with open(file_ram_stats, 'a+') as f:
                f.write('RAM usage: ' + str(misuration_ram_usage) + "\n")
            self.total_RAM_usages.append(misuration_ram_usage)
            time.sleep(300)                                                                    # I go to sleep for 5 minutes so that the stats are printed every 5 minutes and not repeatedly
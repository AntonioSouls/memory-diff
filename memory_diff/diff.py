from difflib import ndiff
from bs4 import BeautifulSoup

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:
    # CLASS CONSTRUCTOR: the object takes three files as parameters, where the first one we insert is the "new" one, the second one is the "old" one, the third one is the file in which 
    # we save the differences
    def __init__(self,file_new: str, file_old:str, file_diff:str) -> None: 
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.list_file_new = []
        self.list_file_old = []
        self.list_file_diff = []

    # Doing diff between two files: an Old File and a New File and saving into a third file only the differences between the preavious files
    def diff_function(self):
        with open(self.file_new, 'r') as file_object_new:                      # Opening the new file for reading
            self.list_file_new = file_object_new.read()
        with open(self.file_old, 'r') as file_object_old:                      # Opening the old file for reading
            self.list_file_old = file_object_old.read()
        

        Bs_data_new = BeautifulSoup(self.list_file_new, "tmx")                 # Passing the stored data inside the beautifulsoup parser, storing the returned object
        Bs_data_old = BeautifulSoup(self.list_file_old, "tmx")
        
        
                                                                              # Starting the research of the differences between two files
        for string_new in self.list_file_new:
            exist: bool = False
            i:int = 0
            while i<len(self.list_file_old) and exist == False:
                if string_new == self.list_file_old[i] :
                    exist = True
                i=i+1
            if(not exist):
                self.list_file_diff.append(string_new)

                                                                            # Saving the differences into a third file called diff_file
        file_object_diff = open(self.file_diff, 'w')
        file_object_diff.writelines(self.list_file_diff)
        file_object_diff.close()                                             
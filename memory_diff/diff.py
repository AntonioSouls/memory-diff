from difflib import ndiff

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:
    # CLASS CONSTRUCTOR: the object takes three files as parameters, where the first one we insert is the "new" one, the second one is the "old" one, the third one is the file in which 
    # we save the differences
    def __init__(self,file_new: str, file_old:str, file_diff:str) -> None: 
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.lista_file_new = None
        self.lista_file_old = None
        self.lista_file_diff = []

    # Doing diff between two files: an Old File and a New File and saving into a third file only the differences between the preavious files
    def diff_function(self):
        file_object_new = open(self.file_new, 'r')                             # Opening the new file for reading
        file_object_old = open(self.file_old, 'r')                             # Opening the old file for reading
        self.lista_file_new = file_object_new.readlines()                      # Saving the new file's lines into a list
        self.lista_file_old = file_object_old.readlines()                      # Saving the old file's lines into a list
        file_object_new.close()                                                # Closing the new file
        file_object_old.close()                                                # Closing the old file
        
                                                                              # Starting the research of the differences between two files
        for stringa_new in self.lista_file_new:
            esiste: bool = False
            i:int = 0
            while i<len(self.lista_file_old) and esiste == False:
                if stringa_new == self.lista_file_old[i] :
                    esiste = True
                i=i+1
            if(esiste==False):
                self.lista_file_diff.append(stringa_new)

                                                                            # Saving the differences into a third file called diff_file
        file_object_diff = open(self.file_diff, 'w')
        file_object_diff.writelines(self.lista_file_diff)
        file_object_diff.close()
        return                                               
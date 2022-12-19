from difflib import ndiff
from bs4 import BeautifulSoup
from memory_diff.components.tu import TranslatedUnit
from memory_diff.components import Tuv
from memory_diff.components import Prop

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:
    # CLASS CONSTRUCTOR: the object takes three files as parameters, where the first one we insert is the "new" one, the second one is the "old" one, the third one is the file in which 
    # we save the differences
    def __init__(self,file_new: str, file_old:str, file_diff:str) -> None: 
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.opened_file_new = None
        self.opened_file_old = None
        self.list_file_diff = []

    # Doing diff between two files: an Old File and a New File and saving into a third file only the differences between the preavious files
    def diff_function(self):
        with open(self.file_new, 'r') as file_object_new:                      # Opening the new file for reading
            self.opened_file_new = file_object_new.read()
        with open(self.file_old, 'r') as file_object_old:                      # Opening the old file for reading
            self.opened_file_old = file_object_old.read()
        

        Bs_data_new = BeautifulSoup(self.opened_file_new, "xml")              # Passing the stored data inside the beautifulsoup parser, storing the returned object
        Bs_data_old = BeautifulSoup(self.opened_file_old, "xml")
        
        new_list_tag_tu = Bs_data_new.find_all('tu')                          # Saving all tag <tu> (with all their descendants) into a list
        old_list_tag_tu = Bs_data_old.find_all('tu')


        # For each tag <tu> of the new list, create an object TranslatedUnit (using the self.build_object_tu()) and compare that object with all the TranslatedUnit
        # of the old list, and, if there is not a match, add the object into another list that contains only the added/modified elements
        for tu_tag in new_list_tag_tu:                                        # Begins loop
            tu_object_new = self.build_object_tu(tu_tag)                      # Creates the object to compare
            exist:bool = False                                                # Does the comparing
            i:int = 0
            while i < len(old_list_tag_tu) and exist == False:
                tu_object_old = self.build_object_tu(old_list_tag_tu[i])
                if tu_object_new == tu_object_old:
                    exist = True
                i=i+1
            if(not exist):
                self.list_file_diff.append(tu_object_new)

        # Saving the differences into a third file called diff_file
        
        ## file_object_diff = open(self.file_diff, 'w')
        ## file_object_diff.writelines(self.list_file_diff)
        ## file_object_diff.close() 



    # Build a TranslatedUnit object. So, thanks this, we can transform a TranslatedUnit block of the XML file into an object 
    def build_object_tu(self, tu_tag):
        tuv_list = tu_tag.find_all('tuv')
        prop_list = tu_tag.find_all('prop')
        prop_first_tag = prop_list[0]
        prop_second_tag = prop_list[1]
        tuv_first_tag = tuv_list[0]
        tuv_second_tag = tuv_list[1]
        prop_first_object = Prop(prop_first_tag['type'],prop_first_tag.string)
        prop_second_object = Prop(prop_second_tag['type'],prop_second_tag.string)
        tuv_first_object = Tuv(tuv_first_tag['xml:lang'],tuv_first_tag.seg.string)
        tuv_second_object = Tuv(tuv_second_tag['xml:lang'],tuv_second_tag.seg.string)
        tu_object = TranslatedUnit(int(tu_tag['tuid']),tu_tag['srclang'],tu_tag['datatype'], tu_tag['creationdate'], tu_tag['changedate'],prop_first_object,prop_second_object,tuv_first_object,tuv_second_object) 
        return tu_object
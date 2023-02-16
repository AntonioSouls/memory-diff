import multiprocessing
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from memory_diff.components.tu import TranslatedUnit
from translate.storage.tmx import tmxfile, tmxunit
from typing import List
from xml.etree.ElementTree import fromstring

# Diff class that models an object that allows you to make the difference between two files and save the difference to another file

class Diff:

    # CLASS CONSTRUCTOR: the object takes three files as parameters, where the first one we insert is the "new" one, the second one is the "old" one, the third one is the file in which 
    # we save the differences
    def __init__(self,file_new:str,file_old:str,file_diff:str) -> None:
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.opened_file_new = None
        self.opened_file_old = None


    # Opens and reads two files on which the diff must be made
    def diff_open_files(self):
        with open(self.file_new, 'rb') as file_object_new:                      # Opening the new file for reading
            self.opened_file_new = tmxfile(file_object_new)
        with open(self.file_old, 'rb') as file_object_old:                      # Opening the old file for reading
            self.opened_file_old = tmxfile(file_object_old)
        
        new_list_tu_object = self.opened_file_new.getunits()                          # Saving all tag <tu> (with all their descendants) into a list
        old_list_tu_object = self.opened_file_old.getunits()

        self.diff_function(new_list_tu_object,old_list_tu_object)                   # Invoking the function that litterally parse both <tu> tag's lists and save into the third one only the differences

    
    # Doing diff between the elements of two lists: a list that contains old tag <tu> and a list that contains new tag <tu> and saving into a third list only the differences between the preavious files
    def diff_function(self, new_list_tu_object,old_list_tu_object):
        pool = multiprocessing.Pool(16)                                                                                                             # Creating a pool of 16 processes to parallelize the diff and make 16 diff at a time
        list_block_diff=[]
        list_processes=list()
        for tu_object_new in new_list_tu_object:                                                                                                                           # I'm parsing the whole list containing the new <tu> blocks and I compare each of these blocks with 
            list_processes.append(pool.apply_async(Diff.view_added_modified_blocks,args=(str(tu_object_new),[str(u) for u in old_list_tu_object])))                        # all the blocks in the old list invoking the view_added_modified_blocks (I made 16 diff at time with the pool)

        for tu_object_old in old_list_tu_object:
            list_processes.append(pool.apply_async(Diff.view_removed_blocks, args=(str(tu_object_old), [str(u) for u in new_list_tu_object])))       #str(tu_object_old),[str(u) for u in new_list_tu_object]
            
        
        pool.close()
        pool.join()
        for process in list_processes:
            res = process.get()
            if res:
                list_block_diff.append(res)
        self.saving_diff(list_block_diff)                                                                                                    # Invoke saving_diff method to save the diff block into a file


   # Comparing a single <tu> block new with all the blocks in the old list. This is for seeing if the new <tu> block has been added or changed. If in the old list there aren't blocks with the same id of the
   # <tu> block new, it means that this block has been added so I have to add it to the list that contains differences. If in the old list there is a block with the same id of <tu> block but change the content
   # of this block, it means that this block has been modified so I have to add it to the list that contains differences. I don't have to add anythink to the list that contains differences only in the case of
   # two block that I'm comparing are perfectly equals
    @staticmethod
    def view_added_modified_blocks(tu_object_new,old_list_tu_object):
        tu_object_new = TranslatedUnit(fromstring(tu_object_new))
        exist:bool = False 
        for i in range(len(old_list_tu_object)):                             
            if exist:
                break
            tu_object_old = TranslatedUnit(fromstring(old_list_tu_object[i]))
            if tu_object_new.__eq__(tu_object_old):
                exist = True
        
        if not exist:
            return str(tu_object_new)
        return None
    

    # Comparing a single <tu> block old with all the blocks in the new list. This is for seeing if the old <tu> block has been removed in the new list. If in the new list there aren't blocks whith the same id
    # of the <tu> block old, it means that the old <tu> block has been removed, so I have to add it to the list that contains differences but added it as a removed block with the removed tag
    @staticmethod
    def view_removed_blocks(tu_object_old,new_list_tu_object):
        tu_object_old = TranslatedUnit(fromstring(tu_object_old))
        same_id:bool = False
        for tu_object_new in new_list_tu_object:                                    
            tu_object_new = TranslatedUnit(fromstring(tu_object_new))
            if same_id:
                break
            if tu_object_old.getId() == tu_object_new.getId():
                same_id = True
        if not same_id:
            object_removed = tu_object_old
            object_removed.setRemoved(True)
            return str(object_removed)
        return None

    
    # Saving the differences into a third file called diff_file
    def saving_diff(self,list_block_diff):
        root = f'<tmx version="1.4">\n'
        header = f'  {self.build_header()}\n'
        body = f'  <body>\n'
        tu_units = f'{self.build_tu(list_block_diff)}\n'
        body_end = f'  </body>'
        root_end = f'</tmx>'

        diff_tmx = root + header + body + tu_units + body_end + root_end                                              
        bs_data = BeautifulSoup(diff_tmx, 'xml')                                  
        xml = bs_data.prettify("UTF-8")                                           

        with open(self.file_diff, 'wb') as f:                                     
            f.write(xml)
    

    # Method that helps self.saving_diff() to create the header part of the diff file
    def build_header(self):
        with open(self.file_new, 'r') as f:
            data = f.read()
        Bs_data_new = BeautifulSoup(data, "xml")                  # Using new file to discover the value of header's attributes
        tag_header_of_new_file = Bs_data_new.find('header')
        return tag_header_of_new_file
    

    # Method that helps self.saving_diff() to create the Translated Unit part of the diff file
    def build_tu(self,list_block_diff):
        tu_units:str = ""
        for tu_object in list_block_diff:                                       # Add a complete <tu> tag with all attributes and all sub-tags for each tu_object that have into list 
            if(tu_object is not None):
                tu_units = tu_units + tu_object
        return tu_units
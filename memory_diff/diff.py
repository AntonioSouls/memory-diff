import multiprocessing
from bs4 import BeautifulSoup
from memory_diff.components.tu import TranslatedUnit
from translate.storage.tmx import tmxfile
from typing import List
from xml.etree.ElementTree import fromstring
from tqdm import tqdm
import threading
from lxml import etree


# Diff class which, taking three input files, makes the difference between the first two and saves the differences on the third
class Diff:

    # Constructor of the class to take as input the three files of which:
    # - The new file will be first
    # - The second will be the old file
    # - The third will be the file where we save the differences
    def __init__(self,file_new:str,file_old:str,file_diff:str) -> None:
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.num_workers = 32                             # I impose that 32 processes are created and, therefore, that 32 <tu> can be analyzed at a time (no more because it could be too expensive)
        self.opened_file_new = None
        self.opened_file_old = None


    # Function that takes care of opening the two files on which to make the diff and saving their content in a corresponding dictionary, in order to make it easy to access the units of the single file
    def diff_open_files(self):
        
        
        with open(self.file_new, 'rb') as file_object_new:                                          # Open new file
            self.opened_file_new = file_object_new.read()
        with open(self.file_old, 'rb') as file_object_old:                                          # Open old file
            self.opened_file_old = file_object_old.read()

        parser = etree.XMLParser(recover=True)                                                     # Creation of a parser that will analyzei f there are UNICODE errors into the files and, if there are, it fixed them

        new_tree = etree.fromstring(self.opened_file_new,parser)                                   # Useful steps to make the parser parse the file and fix any UNICODE errors
        old_tree = etree.fromstring(self.opened_file_old,parser)

        new_tmx_object = tmxfile.parsestring(etree.tostring(new_tree))
        old_tmx_object = tmxfile.parsestring(etree.tostring(old_tree))
        
        new_list_tu_object = new_tmx_object.getunits()                                            # I create a list containing all the translation units of the file_new                        
        old_list_tu_object = old_tmx_object.getunits()                                            # I create a list containing all the translation units of the file_old
        
        new_dictionary_tu_object = multiprocessing.Manager().dict()                               # Create two dictionaries as global variables
        old_dictionary_tu_object = multiprocessing.Manager().dict()

        
        self.building_dictionary(new_list_tu_object,new_dictionary_tu_object)                     # I invoke the Translation Unit function to populate the two dictionaries starting from the two lists created above
        self.building_dictionary(old_list_tu_object,old_dictionary_tu_object)
        

        self.diff_function(new_dictionary_tu_object,old_dictionary_tu_object)                     # I start the function that will diff between the two dictionaries                

    

    # Function that takes as parameters a list and a reference to a dictionary. For each item in the list, I take its tu_id and create a key-value pair in the dictionary where the key is the tu_id
    # the value is the element of the list.
    # If that element doesn't have a tu_id, I compute the hash of the element and use that hash as the key
    def building_dictionary(self,list_tu_object,dictionary_tu_object):
        for tu_object in tqdm(list_tu_object):
            TranslationUnit_object = TranslatedUnit(fromstring(str(tu_object)))
            if(TranslationUnit_object.getId() is not None):
                lista:list = dictionary_tu_object.get(TranslationUnit_object.getId())
                if(lista is None):
                    lista=list()
                lista.append(TranslationUnit_object)
                dictionary_tu_object[TranslationUnit_object.getId()] = lista
            else:
                hash_TranslationUnit_object = TranslationUnit_object.hash_tu()
                hash_list:list = dictionary_tu_object.get(hash_TranslationUnit_object)
                if(hash_list is None):
                    hash_list = list()
                hash_list.append(TranslationUnit_object)
                dictionary_tu_object[hash_TranslationUnit_object] = hash_list
        return
    


    # Function that diffs between the two dictionaries it receives as parameters and saves the items that differ in a list of differences.
    # Diff is done on 32 units simultaneously
    def diff_function(self, new_dictionary_tu_object,old_dictionary_tu_object):
        
        pool = multiprocessing.Pool(self.num_workers)                                     # I create a pool of 32 processes                                                                                                        
        list_block_diff=[]                                                                # I initialize the list that will contain the differences
        list_processes=list()                                                             # I initialize the list that will contain the results of the processes
        for new_key in tqdm(new_dictionary_tu_object):                                                                                                # Start for each process the function that will see if the single block has been modified, added or remained unchanged                   
            list_processes.append(pool.apply_async(Diff.view_added_modified_blocks,args=(new_key,new_dictionary_tu_object[new_key][0],old_dictionary_tu_object)))                       

        
        for old_key in tqdm(old_dictionary_tu_object):                                                                                                # I start for each process the function that will see if the single block has been removed
            list_processes.append(pool.apply_async(Diff.view_removed_blocks, args=(old_key,new_dictionary_tu_object,old_dictionary_tu_object[old_key][0])))
            
        
        pool.close()
        pool.join()
        for process in list_processes:
            res = process.get()
            if res:
                list_block_diff.append(res)
        self.saving_diff(list_block_diff)                                                                                                  


    # Function which, having taken a key from the new dictionary, sees if the corresponding element has been added, modified or if it has remained the same
    @staticmethod
    def view_added_modified_blocks(key,new_tu_object,old_dictionary_tu_object):
        if key in old_dictionary_tu_object:
            lista = old_dictionary_tu_object[key]
            if new_tu_object == lista[0]:
                return None
        tu_object_diff = new_tu_object
        return str(tu_object_diff)
    

    # Function which, taking a key from the old dictionary, sees if the corresponding element has been removed from the new dictionary
    @staticmethod
    def view_removed_blocks(key,new_dictionary_tu_object,old_tu_object):
        if key in new_dictionary_tu_object:
            return None
        tu_object_diff:TranslatedUnit = old_tu_object
        tu_object_diff.setRemoved(True)
        return str(tu_object_diff)

    
    # Function which, having taken the list of differences, saves them on a file respecting the tmx format
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
    

   # Helper function to saving_diff to build the tmx format header on the file that will contain the differences
    def build_header(self):
        with open(self.file_new, 'r') as f:
            data = f.read()
        Bs_data_new = BeautifulSoup(data, "xml")                  
        tag_header_of_new_file = Bs_data_new.find('header')
        return tag_header_of_new_file
    

    # Saving_diff helper function to transform the objects in the list of differences into tmx format
    def build_tu(self,list_block_diff):
        tu_units:str = ""
        for tu_object in list_block_diff:                                        
            if(tu_object is not None):
                tu_units = tu_units + tu_object
        return tu_units
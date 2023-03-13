import multiprocessing
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from memory_diff.components.tu import TranslatedUnit
from translate.storage.tmx import tmxfile, tmxunit
from typing import List
from xml.etree.ElementTree import fromstring
from tqdm import tqdm
from threading import Thread
import time



class Diff:

    
    def __init__(self,file_new:str,file_old:str,file_diff:str) -> None:
        self.file_new = file_new
        self.file_old = file_old
        self.file_diff = file_diff
        self.num_workers = 32
        self.opened_file_new = None
        self.opened_file_old = None


    
    def diff_open_files(self):
        with open(self.file_new, 'rb') as file_object_new:                      
            self.opened_file_new = tmxfile(file_object_new)
        with open(self.file_old, 'rb') as file_object_old:                      
            self.opened_file_old = tmxfile(file_object_old)
        
        new_list_tu_object = self.opened_file_new.getunits()                          
        old_list_tu_object = self.opened_file_old.getunits()

        new_dictionary_tu_object = multiprocessing.Manager().dict()
        old_dictionary_tu_object = multiprocessing.Manager().dict()

        
        for tu_object_new in new_list_tu_object:
            TranslationUnit_object_new = TranslatedUnit(fromstring(str(tu_object_new)))
            new_dictionary_tu_object[TranslationUnit_object_new.getId()] = TranslationUnit_object_new
        for tu_object_old in old_list_tu_object:
            TranslationUnit_object_old = TranslatedUnit(fromstring(str(tu_object_old)))
            old_dictionary_tu_object[TranslationUnit_object_old.getId()] = TranslationUnit_object_old
        
        
        self.diff_function(new_dictionary_tu_object,old_dictionary_tu_object)                   

  
    def diff_function(self, new_dictionary_tu_object,old_dictionary_tu_object):
        pool = multiprocessing.Pool(self.num_workers)                                                                                                             
        list_block_diff=[]
        list_processes=list()
        for new_key in tqdm(new_dictionary_tu_object):                                                                                                                          
            list_processes.append(pool.apply_async(Diff.view_added_modified_blocks,args=(new_key,new_dictionary_tu_object[new_key],old_dictionary_tu_object)))                       


        for old_key in tqdm(old_dictionary_tu_object):
            list_processes.append(pool.apply_async(Diff.view_removed_blocks, args=(old_key,new_dictionary_tu_object,old_dictionary_tu_object[old_key])))
            
        
        pool.close()
        pool.join()
        for process in list_processes:
            res = process.get()
            if res:
                list_block_diff.append(res)
        self.saving_diff(list_block_diff)                                                                                                  


  
    @staticmethod
    def view_added_modified_blocks(key,new_tu_object,old_dictionary_tu_object):
        
        if key in old_dictionary_tu_object:
            if new_tu_object == old_dictionary_tu_object[key]:
                return None
        tu_object_diff = new_tu_object
        return str(tu_object_diff)
    

   
    @staticmethod
    def view_removed_blocks(key,new_dictionary_tu_object,old_tu_object):
        
        if key in new_dictionary_tu_object:
            return None
        tu_object_diff:TranslatedUnit = old_tu_object
        tu_object_diff.setRemoved(True)
        return str(tu_object_diff)

    
    
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
    

   
    def build_header(self):
        with open(self.file_new, 'r') as f:
            data = f.read()
        Bs_data_new = BeautifulSoup(data, "xml")                  
        tag_header_of_new_file = Bs_data_new.find('header')
        return tag_header_of_new_file
    

    
    def build_tu(self,list_block_diff):
        tu_units:str = ""
        for tu_object in list_block_diff:                                        
            if(tu_object is not None):
                tu_units = tu_units + tu_object
        return tu_units
import multiprocessing
from bs4 import BeautifulSoup
from memory_diff.components.tu import TranslatedUnit
from translate.storage.tmx import tmxfile
from typing import List
from xml.etree.ElementTree import fromstring
from tqdm import tqdm
import threading
from lxml import etree



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
            self.opened_file_new = file_object_new.read()
        with open(self.file_old, 'rb') as file_object_old:                      
            self.opened_file_old = file_object_old.read()

        parser = etree.XMLParser(recover=True)

        new_tree = etree.fromstring(self.opened_file_new,parser)
        old_tree = etree.fromstring(self.opened_file_old,parser)

        new_tmx_object = tmxfile.parsestring(etree.tostring(new_tree))
        old_tmx_object = tmxfile.parsestring(etree.tostring(old_tree))
        
        new_list_tu_object = new_tmx_object.getunits()                          
        old_list_tu_object = old_tmx_object.getunits()
        
        new_dictionary_tu_object = multiprocessing.Manager().dict()
        old_dictionary_tu_object = multiprocessing.Manager().dict()

        
        thread1 = threading.Thread(target=self.building_dictionary,args=(new_list_tu_object,new_dictionary_tu_object))
        thread2 = threading.Thread(target=self.building_dictionary,args=(old_list_tu_object,old_dictionary_tu_object))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        

        self.diff_function(new_dictionary_tu_object,old_dictionary_tu_object)                   

    
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
    

    def diff_function(self, new_dictionary_tu_object,old_dictionary_tu_object):
        pool = multiprocessing.Pool(self.num_workers)                                                                                                             
        list_block_diff=[]
        list_processes=list()
        for new_key in tqdm(new_dictionary_tu_object):                                                                                                                          
            list_processes.append(pool.apply_async(Diff.view_added_modified_blocks,args=(new_key,new_dictionary_tu_object[new_key][0],old_dictionary_tu_object)))                       


        for old_key in tqdm(old_dictionary_tu_object):
            list_processes.append(pool.apply_async(Diff.view_removed_blocks, args=(old_key,new_dictionary_tu_object,old_dictionary_tu_object[old_key][0])))
            
        
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
            lista = old_dictionary_tu_object[key]
            if new_tu_object == lista[0]:
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
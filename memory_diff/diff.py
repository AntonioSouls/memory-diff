from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from memory_diff.components.tu import TranslatedUnit
from memory_diff.components.tuv import Tuv
from memory_diff.components.prop import Prop

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


            ## For each tag <tu> of the new list, create an object TranslatedUnit (using the self.build_object_tu()) and compare that object with all the TranslatedUnit
            ## of the old list, and, if there is not a match, add the object into another list that contains only the added/modified elements
        list_block_diff=[]
        for tu_tag in new_list_tag_tu:                                        # Begins loop
            tu_object_new = TranslatedUnit(tu_tag)                            # Creates the object to compare
            exist:bool = False 
            for i in range(len(old_list_tag_tu)):                             # Does the comparing
                if exist:
                    break
                tu_object_old = TranslatedUnit (old_list_tag_tu[i])
                if tu_object_new == tu_object_old:
                    exist = True
            if not exist:
                list_block_diff.append(tu_object_new)
        
        self.saving_diff(list_block_diff)                                # Invoke saving_diff method to save the diff block into a file

    
    
    # Saving the differences into a third file called diff_file
    def saving_diff(self,list_block_diff):
        root = ET.Element('tmx')                                        # Root Creation
        root.set('version','1.4')                                       # Setting root's attributes
        
        header = ET.SubElement(root,'header')                           # Header Creation as root's subelement 
        header.set('creationtool','MyMemory - Database export tool')    # Setting header's attributes
        header.set('creationtoolversion','1.0')
        header.set('datatype','plaintext')
        header.set('o-tmf','MyMemory')
        header.set('segtype','sentence')
        header.set('adminlang','en-US')
        header.set('srclang','en-GB')

        body = ET.SubElement(header,'body')                             # Body creation as header's subelement

        for tu_object in list_block_diff:
            tu = ET.SubElement(body, 'tu')
            tu.set('tuid',str(tu_object.getId()))
            tu.set('srclang',tu_object.get_srclang())
            tu.set('datatype',tu_object.get_datatype())
            tu.set('creationdate',tu_object.get_creationdate())
            tu.set('changedate',tu_object.get_changedate())
            prop_first = ET.SubElement(tu,'prop')
            prop_second = ET.SubElement(tu,'prop')
            tuv_first = ET.SubElement(tu,'tuv')
            tuv_second = ET.SubElement(tu,'tuv')
            prop_first.set('type',tu_object.get_prop_first().getType())
            prop_first.text = tu_object.get_prop_first().getContent()
            prop_second.set('type',tu_object.get_prop_second().getType())
            prop_second.text = tu_object.get_prop_second().getContent()
            tuv_first.set('xml:lang',tu_object.get_tuv_first().get_xml())
            seg_first = ET.SubElement(tuv_first, 'seg')
            seg_first.text = tu_object.get_tuv_first().getContent()
            tuv_second.set('xml:lang',tu_object.get_tuv_second().get_xml())
            seg_second = ET.SubElement(tuv_second, 'seg')
            seg_second.text = tu_object.get_tuv_second().getContent()
        
        diff_tmx = ET.tostring(root)

        with open(self.file_diff, 'wb') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>')
            f.write(diff_tmx)
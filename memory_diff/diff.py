from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from memory_diff.components.tu import TranslatedUnit
from memory_diff.components.tuv import Tuv
from memory_diff.components.prop import Prop

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
        
        for tu_tag_old in old_list_tag_tu:
            same_id:bool = False
            for tu_tag_new in new_list_tag_tu:
                if same_id:
                    break
                if tu_tag_old['tuid'] == tu_tag_new['tuid']:
                    same_id = True
            if not same_id:
                object_removed = TranslatedUnit(tu_tag_old)
                object_removed.setRemoved(True)
                list_block_diff.append(object_removed)
        
        self.saving_diff(list_block_diff)                                # Invoke saving_diff method to save the diff block into a file

    
    
    # Saving the differences into a third file called diff_file
    def saving_diff(self,list_block_diff):
        root = ET.Element('tmx')                                                  # Root Creation
        root.set('version','1.4')                                                 # Setting root's attributes
        self.build_header(root)                                                   # Header creation as root's subelement
        body = ET.SubElement(root,'body')                                         # Body creation as root's subelement
        self.build_tu(list_block_diff,body)

        diff_tmx = ET.tostring(root)                                              # Create a string to represent the just created xml file
        bs_data = BeautifulSoup(diff_tmx, 'xml')                                  # Transform that string into a beautiful soup element that we use to correctly identify the xml file
        xml = bs_data.prettify("UTF-8")                                           # Identify the beautiful soup correctly

        with open(self.file_diff, 'wb') as f:                                     # Saving into a file the Beautiful Soup object correctly identified
            f.write(xml)
    

    # Method that helps self.saving_diff() to create the header part of the diff file
    def build_header(self,root):
        Bs_data_new = BeautifulSoup(self.opened_file_new, "xml")                  # Using new file to discover the value of header's attributes
        tag_header_of_new_file = Bs_data_new.find('header')
        header = ET.SubElement(root,'header')                                     # Header Creation as root's subelement 
        header.set('creationtool',tag_header_of_new_file['creationtool'])         # Setting header's attributes
        header.set('creationtoolversion',tag_header_of_new_file['creationtoolversion'])
        header.set('datatype',tag_header_of_new_file['datatype'])
        header.set('o-tmf',tag_header_of_new_file['o-tmf'])
        header.set('segtype',tag_header_of_new_file['segtype'])
        header.set('adminlang',tag_header_of_new_file['adminlang'])
        header.set('srclang',tag_header_of_new_file['srclang'])
    

    # Method that helps self.saving_diff() to create the Translated Unit part of the diff file
    def build_tu(self,list_block_diff,body):
        for tu_object in list_block_diff:                                      # Add a complete <tu> tag with all attributes and all sub-tags for each tu_object that have into list 
            tu = ET.SubElement(body, 'tu')
            tu.set('tuid',str(tu_object.getId()))
            if tu_object.get_srclang() != None:
                tu.set('srclang',tu_object.get_srclang())
            if tu_object.get_datatype() != None:
                tu.set('datatype',tu_object.get_datatype())
            if tu_object.get_creationdate() != None:
                tu.set('creationdate',tu_object.get_creationdate())
            if tu_object.get_changedate() != None:
                tu.set('changedate',tu_object.get_changedate())
            if tu_object.getRemoved() != None :
                tu.set('removed','True')
            prop_first = ET.SubElement(tu,'prop')
            prop_first.set('type',tu_object.get_prop_first().getType())
            prop_first.text = tu_object.get_prop_first().getContent()
            if(tu_object.get_prop_second().getType() != None or tu_object.get_prop_second().getContent() != None):
                prop_second = ET.SubElement(tu,'prop')
                prop_second.set('type',tu_object.get_prop_second().getType())
                prop_second.text = tu_object.get_prop_second().getContent()
            tuv_first = ET.SubElement(tu,'tuv')
            tuv_second = ET.SubElement(tu,'tuv')
            tuv_first.set('xml:lang',tu_object.get_tuv_first().get_xml())
            seg_first = ET.SubElement(tuv_first, 'seg')
            seg_first.text = tu_object.get_tuv_first().getContent()
            tuv_second.set('xml:lang',tu_object.get_tuv_second().get_xml())
            seg_second = ET.SubElement(tuv_second, 'seg')
            seg_second.text = tu_object.get_tuv_second().getContent()
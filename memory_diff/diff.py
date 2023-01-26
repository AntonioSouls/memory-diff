import multiprocessing
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from memory_diff.components.tu import TranslatedUnit

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
        with open(self.file_new, 'r') as file_object_new:                      # Opening the new file for reading
            self.opened_file_new = file_object_new.read()
        with open(self.file_old, 'r') as file_object_old:                      # Opening the old file for reading
            self.opened_file_old = file_object_old.read()
        

        Bs_data_new = BeautifulSoup(self.opened_file_new, "xml")              # Passing the stored data inside the beautifulsoup parser, storing the returned object
        Bs_data_old = BeautifulSoup(self.opened_file_old, "xml")
        
        new_list_tag_tu = Bs_data_new.find_all('tu')                          # Saving all tag <tu> (with all their descendants) into a list
        old_list_tag_tu = Bs_data_old.find_all('tu')
       
        self.diff_function(new_list_tag_tu,old_list_tag_tu)                   # Invoking the function that litterally parse both <tu> tag's lists and save into the third one only the differences

    
    # Doing diff between the elements of two lists: a list that contains old tag <tu> and a list that contains new tag <tu> and saving into a third list only the differences between the preavious files
    def diff_function(self, new_list_tag_tu,old_list_tag_tu):
        pool = multiprocessing.Pool(process=16)                                                                                           # Creating a pool of 16 processes to parallelize the diff and make 16 diff at a time
        list_block_diff=[]
        list_processes =[]
        for tu_tag in new_list_tag_tu:                                                                                                    # I'm parsing the whole list containing the new <tu> blocks and I compare each of these blocks with 
            list_processes.append(pool.apply_async(self.view_added_modified_blocks,args=(tu_tag,old_list_tag_tu)))                        # all the blocks in the old list invoking the view_added_modified_blocks (I made 16 diff at time with the pool)


        for tu_tag_old in old_list_tag_tu:
            list_processes.append(pool.apply_async(self.view_removed_blocks, args=(tu_tag_old,new_list_tag_tu)))
            

        pool.close()                                                                                                                        # Closing the pool
        pool.join()       
        for process in list_processes:
            list_block_diff.append(process.get())
        self.saving_diff(list_block_diff)                                                                                                    # Invoke saving_diff method to save the diff block into a file


   # Comparing a single <tu> block new with all the blocks in the old list. This is for seeing if the new <tu> block has been added or changed. If in the old list there aren't blocks with the same id of the
   # <tu> block new, it means that this block has been added so I have to add it to the list that contains differences. If in the old list there is a block with the same id of <tu> block but change the content
   # of this block, it means that this block has been modified so I have to add it to the list that contains differences. I don't have to add anythink to the list that contains differences only in the case of
   # two block that I'm comparing are perfectly equals
    def view_added_modified_blocks(self,tu_tag,old_list_tag_tu):
            tu_object_new = TranslatedUnit(tu_tag)                            # Creates the object to compare
            exist:bool = False 
            for i in range(len(old_list_tag_tu)):                             # Does the comparing
                if exist:
                    break
                tu_object_old = TranslatedUnit (old_list_tag_tu[i])
                if tu_object_new == tu_object_old:
                    exist = True
            if not exist:
                return tu_object_new
            return None
        
    
    # Comparing a single <tu> block old with all the blocks in the new list. This is for seeing if the old <tu> block has been removed in the new list. If in the new list there aren't blocks whith the same id
    # of the <tu> block old, it means that the old <tu> block has been removed, so I have to add it to the list that contains differences but added it as a removed block with the removed tag
    def view_removed_blocks(self,tu_tag_old,new_list_tag_tu):
            same_id:bool = False
            for tu_tag_new in new_list_tag_tu:                                    # Does the comparing
                if same_id:
                    break
                if tu_tag_old['tuid'] == tu_tag_new['tuid']:
                    same_id = True
            if not same_id:
                object_removed = TranslatedUnit(tu_tag_old)
                object_removed.setRemoved(True)
                return object_removed
            return None
    
    
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
            if(tu_object != None):
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
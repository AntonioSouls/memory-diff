from memory_diff.components.prop import Prop
from memory_diff.components.tuv import Tuv
from xml.etree.ElementTree import Element

# TranslatedUnit class that models an object that simulate the behavior of <tu> tag

class TranslatedUnit:

    def __init__(self,tu_tmx:Element) -> None:
        self.tuid = tu_tmx.get("tuid")
        self.srclang = tu_tmx.get("srclang")
        self.datatype = tu_tmx.get("datatype")
        self.creationdate = tu_tmx.get("creationdate")
        self.changedate = tu_tmx.get("changedate")
        self.removed = None

        tuv_tag_list = tu_tmx.findall('tuv')
        self.tuv_first = Tuv(tuv_tag_list[0])
        self.tuv_second = Tuv(tuv_tag_list[1])
        
        prop_tag_list = tu_tmx.findall("prop")
        if len(prop_tag_list) == 1:
            prop_first_object = Prop(prop_tag_list[0])
            prop_second_object = Prop(None)
        else:
            prop_first_object = Prop(prop_tag_list[0])
            prop_second_object = Prop(prop_tag_list[1])
        
        self.prop_first = prop_first_object
        self.prop_second = prop_second_object

    def getId(self):
        return self.tuid
    def setId(self, id:int):
        self.tuid = id
    
    def getRemoved(self):
        return self.removed
    def setRemoved(self, removed:bool):
        self.removed = removed
    
    def get_srclang(self):
        return self.srclang
    def set_srclang(self,srclang:str):
        self.srclang = srclang
    
    def get_datatype(self):
        return self.datatype
    def set_datatype(self,datatype:str):
        self.datatype = datatype
    
    def get_creationdate(self):
        return self.creationdate
    def set_creationdate(self, creationdate:str):
        self.creationdate = creationdate
    
    def get_changedate(self):
        return self.changedate
    def set_changedate(self, changedate:str):
        self.changedate = changedate
    
    def get_prop_first(self):
        return self.prop_first
    def set_prop_first(self,prop_one: Prop):
        self.prop_first = prop_one
    
    def get_prop_second(self):
        return self.prop_second
    def set_prop_second(self, prop_two: Prop):
        self.prop_second = prop_two
    
    def get_tuv_first(self):
        return self.tuv_first
    def set_tuv_first(self, tuv_one:Tuv):
        self.tuv_first = tuv_one
    
    def get_tuv_second(self):
        return self.tuv_second
    def set_tuv_second(self, tuv_two:Tuv):
        self.tuv_second = tuv_two
    
    
    
    def __eq__(self,translated_unit_old):   
        equals: bool = False
        if self.tuid == translated_unit_old.getId():
            if self.srclang == translated_unit_old.get_srclang() and self.datatype == translated_unit_old.get_datatype() and self.creationdate == translated_unit_old.get_creationdate() and self.changedate == translated_unit_old.get_changedate():
                if self.tuv_first == translated_unit_old.get_tuv_first() and self.tuv_second == translated_unit_old.get_tuv_second():
                    if self.prop_first == translated_unit_old.get_prop_first():
                        if ((self.prop_second is None) and (translated_unit_old.get_prop_second() is None)) or ((self.prop_second is not None) and (translated_unit_old.get_prop_second() is not None) and (self.prop_second == translated_unit_old.get_prop_second())):
                            equals = True
        return equals

    def __str__(self) -> str:
        toString1 = f'    <tu tuid="{self.getId()}" srclang="{self.get_srclang()}" datatype="{self.get_datatype()}" creationdate="{self.get_creationdate()}" changedate="{self.get_changedate()}" removed="{self.getRemoved()}">\n      <prop type="{self.get_prop_first().getType()}">{self.get_prop_first().getContent()}</prop>\n'
        if(self.get_prop_second() is not None):
            toString2 = f'      <prop type="{self.get_prop_second().getType()}">{self.get_prop_second().getContent()}</prop>\n'
            toString1 = toString1 + toString2
        toString3 = f'      <tuv xml:lang="{self.get_tuv_first().get_xml()}">\n        <seg>{self.get_tuv_first().getContent()}</seg>\n      </tuv>\n      <tuv xml:lang="{self.get_tuv_second().get_xml()}">\n        <seg>{self.get_tuv_second().getContent()}</seg>\n      </tuv>\n    </tu>\n'
        toString = toString1 + toString3
        return toString
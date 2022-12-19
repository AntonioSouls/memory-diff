from memory_diff.components import Prop
from memory_diff.components import Tuv

# TranslatedUnit class that models an object that simulate the behavior of <tu> tag

class TranslatedUnit:

    def __init__(self,tuid:int,srclang:str,datatype:str, creationdate:str, changedate:str, prop1:Prop, prop2:Prop,tuv1:Tuv,tuv2:Tuv) -> None:
        self.tuid = tuid
        self.srclang = srclang
        self.datatype = datatype
        self.creationdate = creationdate
        self.changedate = changedate
        self.prop_first = prop1
        self.prop_second = prop2
        self.tuv_first = tuv1
        self.tuv_second = tuv2

    def getId(self):
        return self.tuid
    def setId(self, id:int):
        self.tuid = id
    
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
    
    
    
    def __eq__(self,translated_unit_old):   # DEFINIRE BENE LA LOGICA DI QUESTO EQUALS PERCHE' E' IMPORTANTE
        if self.tuid == translated_unit_old.getId():
            if self.srclang == translated_unit_old.get_srclang() and self.datatype == translated_unit_old.get_datatype() and self.creationdate == translated_unit_old.get_creationdate() and self.changedate == translated_unit_old.get_changedate():
                if self.prop_first == translated_unit_old.get_prop_first and self.prop_second == translated_unit_old.get_prop_second():
                    if self.tuv_first == translated_unit_old.get_tuv_first() and self.tuv_second == translated_unit_old.get_tuv_second():
                        return True
                    return False
                return False
            return False
        return False
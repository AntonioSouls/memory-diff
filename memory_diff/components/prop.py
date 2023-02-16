from xml.etree.ElementTree import Element

# Prop class that models an object that simulate the behavior of <prop> tag

class Prop:
    def __init__(self, prop_tmx:Element) -> None:
        if prop_tmx is None:
            self.type = None
            self.content = None
        else:
            self.type = prop_tmx.get("type") 
            self.content = prop_tmx.text 

    def getType(self):
        return self.type
    def setType(self, type:str):
        self.type = type
    
    def getContent(self):
        return self.content
    def setContent(self, content:str):
        self.content = content

    def __eq__(self,prop_old):
        if self.content == prop_old.getContent() and self.type == prop_old.getType():
            return True
        return False
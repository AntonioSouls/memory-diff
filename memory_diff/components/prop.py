

# Prop class that models an object that simulate the behavior of <prop> tag

class Prop:
    def __init__(self, prop_tag=None) -> None:
        if prop_tag:
            self.type = prop_tag['type']
            self.content = prop_tag.string
        else:
            self.type = None
            self.content = None

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
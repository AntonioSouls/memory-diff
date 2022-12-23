

# Prop class that models an object that simulate the behavior of <prop> tag

class Prop:
    def __init__(self, prop_tag=None) -> None:
        self.type = prop_tag['type'] if prop_tag else None
        self.content = prop_tag.string if prop_tag else None

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
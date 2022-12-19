

# Prop class that models an object that simulate the behavior of <prop> tag

class Prop:
    def __init__(self, type:str, content:str) -> None:
        self.type = type
        self.content = content

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
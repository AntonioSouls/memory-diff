

# Tuv class that models an object that simulate the behavior of <tuv> tag

class Tuv:
    def __init__(self, xml_lang: str, content: str) -> None:
        self.xml_lang = xml_lang
        self.content = content
    
    def get_xml(self):
        return self.xml_lang
    def set_xml(self, xml:str):
        self.xml_lang = xml

    def getContent(self):
        return self.content
    def setContent(self, content:str):
        self.content = content
    
    def __eq__(self, tuv_old):
        if self.xml_lang == tuv_old.get_xml and self.content == tuv_old.getContent:
            return True
        return False
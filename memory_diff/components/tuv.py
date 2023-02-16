from xml.etree.ElementTree import Element

# Tuv class that models an object that simulate the behavior of <tuv> tag

class Tuv:
    def __init__(self,tuv_tmx:Element) -> None:
        if(tuv_tmx is None):
            self.xml_lang = None
            self.content = None
        else:
            xml_lang = tuv_tmx.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            self.xml_lang = xml_lang
            seg_tmx = tuv_tmx.findall("seg")
            self.content = seg_tmx[0].text
    
    def get_xml(self):
        return self.xml_lang
    def set_xml(self, xml:str):
        self.xml_lang = xml

    def getContent(self):
        return self.content
    def setContent(self, content:str):
        self.content = content
    
    def __eq__(self, tuv_old):
        if self.xml_lang == tuv_old.get_xml() and self.content == tuv_old.getContent():
            return True
        return False
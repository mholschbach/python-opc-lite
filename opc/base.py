from lxml import etree
from .parser import Parser
class Base():

    def __init__(self, parent):
        self._parent = parent

    @property
    def parent(self):
        """Returns the parent object of current object"""
        return self._parent
    

class XmlBase():
    def __init__(self):
        self._e = None
        self._parser = Parser()

    @property
    def e(self):
        return self._e
    
    @property
    def parser(self):
        return self._parser
    
    def read(self, f):
        self._e = self._parser.parse(f).getroot()

    def write(self, f):
        f.write(etree.tostring(self.e, encoding='UTF-8', xml_declaration=True, standalone=True))


class PartBase():
    @property
    def package(self):
        return self._parent
    
class XmlTypeobjBase(XmlBase, Base):
    def __init__(self, part):
        XmlBase.__init__(self)
        Base.__init__(self, part)
        self._part = part

    @property
    def part(self):
        return self._part
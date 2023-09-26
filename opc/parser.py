from lxml import etree

class ElementBase(etree.ElementBase):
    @property    
    def ns(self):
        """returns the namespace of the current element"""
        return etree.QName(self).namespace
    
    def qn(self, name, nsmap=None):
        """Returns a fully qualified name of an element based of name and nsmap.
        if nsmap is None, self.nsmap is used. 
        if name has no prefix and nsmap do not have None returns name
        if name has no prefix then nsmap must have None map. 
        """
        if nsmap is None:
            nsmap = self.nsmap

        if ':' in name:
            pfx, name = name.split(':')
        else:
            pfx = None
        
        if (pfx is None) and (None not in nsmap):
            return name
        
        return '{%s}%s' % (nsmap[pfx], name)
    
    @property
    def makeelement(self):
        """returns makeelement method which can be used to create element so that the element base class is used"""
        return Parser().makeelement
    
    def dump(self):
        """dumps the xml string to stdout"""
        return etree.dump(self)

        
class Parser(etree.XMLParser):
    """Parser class that is set with default class lookup for elements"""
    def __init__(self):
        """sets the default element class lookup for the element"""
        self.set_element_class_lookup(etree.ElementDefaultClassLookup(ElementBase))

    def parse(self, fp):
        """parses the given stream of xml and returns the xml tree"""
        return etree.parse(fp, self)
        


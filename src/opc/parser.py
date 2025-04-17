from lxml import etree
from lxmlutil.etree import ElementBase


class Parser(etree.XMLParser):
    """Parser class that is set with default class lookup for elements"""

    def __init__(self) -> None:
        """sets the default element class |eb| lookup  for the element"""
        self.set_element_class_lookup(etree.ElementDefaultClassLookup(ElementBase))

    def parse(self, fp):  # type: ignore[no-untyped-def]
        """parses the given file object and returns the xml tree"""
        return etree.parse(fp, self)

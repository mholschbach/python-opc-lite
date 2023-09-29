from lxml import etree


class ElementBase(etree.ElementBase):
    """Default base class to be used while creating python objects for the xml
    elements. Providing default base class is useful to add some methods and
    properties to the python objects of the xml elements.
    """

    @property
    def ns(self):
        """Readonly property.

        :returns: namespace of the element
        """
        return etree.QName(self).namespace

    def qn(self, name, nsmap=None):
        """Handy method to get a qualified name from given arguments

        :param name: prefixed or un-prefixed element name.
        :param nsmap: dict with key as prefix and value as namespace
        :returns: fully qualified name (qn).

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
        """Readonly property.

        :returns: makeelement method of the |parser| which can be used to \
create element so that the element base class is used

        """
        return Parser().makeelement

    def dump(self):
        """dumps the xml string to stdout"""
        return etree.dump(self)


class Parser(etree.XMLParser):
    """Parser class that is set with default class lookup for elements"""

    def __init__(self):
        """sets the default element class |eb| lookup  for the element"""
        self.set_element_class_lookup(
            etree.ElementDefaultClassLookup(ElementBase))

    def parse(self, fp):
        """parses the given file object and returns the xml tree"""
        return etree.parse(fp, self)

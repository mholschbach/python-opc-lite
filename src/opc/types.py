from .base import Base, XmlBase
from .uri import Uri


class Types(XmlBase, Base):
    """Class representing the "[Content_Types].xml" file in the |package|.
    Inherits XmlBase and Base classes
    """

    zipname = '[Content_Types].xml'

    def __init__(self, parent):
        Base.__init__(self, parent)
        XmlBase.__init__(self)

    def remove_type(self, uri_str):
        """Removes the type for given uri_str. If uri_str presents in Override
        elements of xml, that Override element would be removed. Otherwise
        Default element would be removed having the same extension as uri_str.

        :param uri_str: string value of the part's uri
        """
        for e in self.e.findall('{*}Override'):
            if e.get('PartName') == uri_str:
                e.getparent().remove(e)
                return
        extension = Uri(uri_str).ext
        for e in self.e.findall('{*}Default'):
            if e.get('Extension').lower() == extension.lower():
                e.getparent().remove(e)
                return

    def get_type(self, uri_str):
        """Returns the type of given uri_str. First Override elements in xml
        are checked for match then Default elements are checked

        :param uri_str: string value of the part's uri
        :returns: string value of the type of the given uri_str
        """
        for e in self.e.findall('{*}Override'):
            if e.get('PartName') == uri_str:
                return e.get('ContentType')

        extension = Uri(uri_str).ext
        for e in self.e.findall('{*}Default'):
            if e.get('Extension').lower() == extension.lower():
                return e.get('ContentType')

    def add_default(self, part):
        """Adds the content type and extension of the part to the xml

        :param part: |part| object
        """
        attrib = {'Extension': part.uri.ext, 'ContentType': part.type}
        for e in self.e.findall('{*}Default'):
            if e.attrib == attrib:
                return
        self.e.insert(0, self.parser.makeelement(self.e.qn('Default'),
                                                 **attrib))

    def add_override(self, part):
        """Add the uri_str and type of the part to the xml

        :param part: part object
        """
        attrib = {'PartName': part.uri.str, 'ContentType': part.type}
        for e in self.e.findall('{*}Override'):
            if e.attrib == attrib:
                return
        self.e.append(self.parser.makeelement(self.e.qn('Override'), **attrib))

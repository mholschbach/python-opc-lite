from .base import Base, XmlBase
from .part import Part
from .uri import Uri


class Types(XmlBase, Base):
    """Class representing the "[Content_Types].xml" file in the |package|.
    Inherits XmlBase and Base classes
    """

    zipname = "[Content_Types].xml"

    def __init__(self, parent: object):
        Base.__init__(self, parent)
        XmlBase.__init__(self)

    def remove_type(self, uri_str: str) -> None:
        """Removes the type for given uri_str. If uri_str presents in Override
        elements of xml, that Override element would be removed. Otherwise
        Default element would be removed having the same extension as uri_str.

        :param uri_str: string value of the part's uri
        """
        if self.e is None:
            return None

        for e in self.e.findall("{*}Override"):
            if e.get("PartName") == uri_str:
                if (parent := e.getparent()) is not None:
                    parent.remove(e)
                return None
        uri_extension = Uri(uri_str).ext
        for e in self.e.findall("{*}Default"):
            if (extension := e.get("Extension")) is not None:
                if extension.lower() == uri_extension.lower():
                    if (parent := e.getparent()) is not None:
                        parent.remove(e)
                return None

    def get_type(self, uri_str: str) -> str | None:
        """Returns the type of given uri_str. First Override elements in xml
        are checked for match then Default elements are checked

        :param uri_str: string value of the part's uri
        :returns: string value of the type of the given uri_str
        """
        if self.e is None:
            return None

        for e in self.e.findall("{*}Override"):
            if e.get("PartName") == uri_str:
                return e.get("ContentType")

        uri_extension = Uri(uri_str).ext
        for e in self.e.findall("{*}Default"):
            if (extension := e.get("Extension")) is not None:
                if extension.lower() == uri_extension.lower():
                    return e.get("ContentType")

        return None

    def add_default(self, part: Part) -> None:
        """Adds the content type and extension of the part to the xml

        :param part: |part| object
        """
        attrib = {"Extension": part.uri.ext, "ContentType": part.type}

        if self.e is None:
            return None

        for e in self.e.findall("{*}Default"):
            if e.attrib == attrib:
                return
        self.e.insert(0, self.parser.makeelement(self.e.qn("Default"), **attrib))  # type: ignore[attr-defined,arg-type]

    def add_override(self, part: Part) -> None:
        """Add the uri_str and type of the part to the xml

        :param part: part object
        """
        attrib = {"PartName": str(part.uri), "ContentType": part.type}

        if self.e is None:
            return None

        for e in self.e.findall("{*}Override"):
            if e.attrib == attrib:
                return
        self.e.append(self.parser.makeelement(self.e.qn("Override"), **attrib))  # type: ignore[attr-defined,arg-type]

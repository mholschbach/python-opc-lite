from .base import Base, PartBase
from .uri import Uri


class Part(PartBase, Base):
    """Part class is not to be instantiated directly. Instead use |add_part|

    :param parent: package object
    :param uri_str: uri string
    :param type: type of content of part
    """

    def __init__(self, parent, uri_str, type_):
        super().__init__(parent)
        self._uri = Uri(uri_str)
        self._type = type_
        self._typeobj = None
        self._data = None

    @property
    def uri(self):
        """Readonly property

        :returns: |uri| object of the part
        """
        return self._uri

    @property
    def type(self):
        """Readonly property

        :returns: content type of the part
        """
        return self._type

    @property
    def typeobj(self):
        """Readonly property

        :getter: object created as per the content of the part using hook
        :setter: sets the typeobj property of part
        """
        return self._typeobj

    @typeobj.setter
    def typeobj(self, typeobj_):
        """sets the typeobj property of Part to given value"""
        self._typeobj = typeobj_

    def read(self, f):
        """reads the content from the file object. if typeobj is present
        then responsibility of reading the content is passed on to typeobj

        :param f: file object
        """
        if self.typeobj is None:
            self._data = f.read()
        else:
            self.typeobj.read(f)

    def write(self, f):
        """writes the part content to the file object. if typeobj is present
        then responsibility of writing the content is passed on to typeobj

        :param f: file object
        """
        if self.typeobj is None:
            f.write(self._data)
        else:
            self.typeobj.write(f)

    def get_rels_part(self):
        """Method that gets the |relspart|  of the current part

        :returns: |relspart| object or None

    Example::

        from opc import Package
        package = Package("/some/path/to/presentation.pptx").read()
        presentation_part = package.get_part('/ppt/presentation.xml')
        print(presentation_part.uri.str)    # '/ppt/presentation.xml'

        presentation_relspart = presentation_part.get_rels_part()
        print(presentation_relspart.uri.str) # /ppt/_rels/presentation.xml.rels
        """
        return self.parent.get_part(self.uri.rels)

    def get_abs_uri_str(self, target_rel_uri_str):
        """Method to get the absolute uri string value from the given relative
        uri string value of target part

        :param target_rel_uri_str: relative uri string value of a target part
        :returns: absolute uri string value of a target part

    Example::

        abs_uri_str = presentation_part.get_abs_uri_str('slides/slide1.xml)
        print(abs_uri_str)      # /ppt/slides/slide1.xml
        """
        if target_rel_uri_str:
            return self.uri.get_abs(target_rel_uri_str)

    def get_related_part(self, rid):
        """Method to get the part object from the relationship id with respect
        to current part.

        :param rid: relationship id
        :returns: the related |part| of the current part from the relationship

    Example::

        related_part = presentation_part.get_related_part('rId2')
        print(related_part.uri.str)     # /ppt/slides/slide1.xml
        """
        rels_part = self.get_rels_part()
        if rels_part is None:
            return
        target_rel_uri_str = rels_part.get_target_rel_uri_str(rid)
        related_part_uri_str = self.get_abs_uri_str(target_rel_uri_str)
        return self.parent.get_part(related_part_uri_str)

from .base import Base, PartBase
from .uri import Uri

class Part(PartBase, Base):
    """Part class is not to be instantiated directly. Instead use Package.add_part()"""
    def __init__(self, parent, uri_str, type_):
        super().__init__(parent)
        self._uri = Uri(uri_str)
        self._type = type_
        self._typeobj = None
        self._data = None

    @property
    def uri(self):
        """uri property of Part object"""
        return self._uri
    
    @property
    def type(self):
        """type property of Part object"""
        return self._type
    
    @property
    def typeobj(self):
        """typeobj property of Part object. It is created as per the hooks registered in package"""
        return self._typeobj
    
    @typeobj.setter
    def typeobj(self, typeobj_):
        """sets the typeobj property of Part to given value"""
        self._typeobj = typeobj_

    def read(self, f):
        """reads the part content from the stream"""
        if self.typeobj is None:
            self._data = f.read()
        else:
            self.typeobj.read(f)

    def write(self, f):
        """writes the part content to the stream"""
        if self.typeobj is None:
            f.write(self._data)
        else:
            self.typeobj.write(f)

    def get_rels_part(self):
        """returns the rels part of the current part object """
        return self.parent.get_part(self.uri.rels)

    def get_abs_uri_str(self, target_rel_uri_str):
        """returns the absolute uri string value from the given relative uri string value of target part"""
        if target_rel_uri_str:
            return self.uri.get_abs(target_rel_uri_str)
        
    def get_related_part(self, rid):
        """returns the related part of the current part from the relationship id (rid)"""
        rels_part = self.get_rels_part()
        if rels_part is None:
            return
        target_rel_uri_str = rels_part.get_target_rel_uri_str(rid)
        related_part_uri_str = self.get_abs_uri_str(target_rel_uri_str)
        return self.parent.get_part(related_part_uri_str)
        
    

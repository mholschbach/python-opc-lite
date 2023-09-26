from zipfile import ZipFile, ZIP_DEFLATED
from .types import Types
from .base import Base
from .part import Part
from .relspart import RelsPart
from .rels import Relationships
from .coreprops import CoreProperties
from .uri import Uri

class Package(Base):
    """Light weight class representing OPC(Open Package Convention) for Office Open XML packages"""

    def __init__(self, path, parent=None):
        """Initiates the properties of Package object and registers hooks for 
        relationships and core-properties part"""
        super().__init__(parent)
        self._path = path
        self._parts = dict()
        self._types = Types(self)
        self._part_hooks = dict()
        self.register_part_hook(RelsPart.type, Relationships)
        self.register_part_hook(CoreProperties.type, CoreProperties)

    @property
    def path(self):
        """returns the path of the package file"""
        return self._path
    
    @property
    def types(self):
        """Returns the content types object of the package"""
        return self._types

    @property
    def core_properties(self):
        return self.get_part('/docProps/core.xml').typeobj
    
    def read(self):
        """Reads the package file and constructs the part objects"""
        with ZipFile(self.path, 'r') as zr:
            with zr.open(self.types.zipname, 'r') as f:
                self.types.read(f)

            for zipname in zr.namelist():
                if zipname == self.types.zipname:
                    continue
                
                uri_str = Uri.zipname2str(zipname)
                part = self.add_part(uri_str, self.types.get_type(uri_str))
                with zr.open(zipname, 'r') as f:
                    part.read(f)
        return self

    def write(self, path):
        """Writes the package to given path"""
        with ZipFile(path, 'w', compression=ZIP_DEFLATED) as zw:
            for part in self._parts.values():
                zipname = part.uri.zipname
                with zw.open(zipname, 'w') as f:
                    part.write(f)

            with zw.open(self.types.zipname, 'w') as f:
                self.types.write(f)

    def exists_part(self, uri_str):
        """Returns if part exists in the package with given uri_str"""
        return uri_str in self._parts

    def add_part(self, uri_str, type_):
        """Adds part or relspart to the package with given uri
        if class
        """
        if self.exists_part(uri_str):
            raise ValueError("Part already exists with given uri")
        
        uri = Uri(uri_str)
        part_class = Part
        if uri.is_rels:
            part_class = RelsPart   # to have some specific methods for relspart

        part = part_class(self, uri_str, type_)
        self._parts[uri_str] = part

        if type_ in self._part_hooks:
            hook = self._part_hooks[type_]
            part.typeobj = hook(part)   # connection between part object and the object per type
        
        return part
            
    def get_part(self, uri_str):
        """Gets part with given uri from the package"""
        if self.exists_part(uri_str):
            return self._parts[uri_str]
    
    def get_parts(self, type_):
        """Returns list of parts of the given content type"""
        return [part for part in self._parts.values() if part.type == type_]
        

    def register_part_hook(self, type_, callback):
        """register a callback hook to the content type. Hooks are called when part is created"""
        self._part_hooks[type_] = callback

    def remove_part(self, uri_str):
        """Removes a part from the package"""
        type = self.get_part(uri_str).type
        del self._parts[uri_str]
        if len(self.get_parts(type)) == 0:
            self._types.remove_type(uri_str)
    




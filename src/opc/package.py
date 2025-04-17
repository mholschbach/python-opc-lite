from pathlib import Path
from typing import Self
from zipfile import ZIP_DEFLATED, ZipFile

from .base import Base, XmlTypeobjBase
from .coreprops import CoreProperties
from .part import Part
from .rels import Relationships
from .relspart import RelsPart
from .types import Types
from .uri import Uri


class Package(Base):
    """Class to handle the office open xml packages as per Open Package
    Convention

    :param path: path of the package file
    :param parent: parent object. default is None

    Example to show how to read and write an opc package::

        from opc import Package

        # create an object of package with path of the file and read contents
        package = Package("/some/path/to/presentation.pptx").read()

        # do some changes to the content of the package

        # write the package to a file
        package.write("/some/other/path/to/saved.pptx")

    """

    _parts: dict[str, Part]
    _part_hooks: dict[str, type[XmlTypeobjBase]]

    def __init__(self, path: Path, parent: object | None = None) -> None:
        """Initiates the properties of Package object and registers hooks for
        |rels| and |cp| part"""
        super().__init__(parent)
        self._path = path
        self._parts = dict()
        self._types = Types(self)
        self._part_hooks = dict()
        self.register_part_hook(RelsPart.type, Relationships)
        self.register_part_hook(CoreProperties.type, CoreProperties)

    @property
    def path(self) -> Path:
        """Readonly property.

        :returns: Path of the package file"""
        return self._path

    @property
    def types(self) -> Types:
        """Readonly property.

        :returns: |ct| object of the package
        """
        return self._types

    @property
    def core_properties(self) -> object | None:
        """Readonly property.

        :returns: |cp| object of the package
        """
        if (part := self.get_part("/docProps/core.xml")) is not None:
            return part.typeobj
        return None

    def read(self) -> Self:
        """Reads the package file and constructs |ct| object and
        |part| of the package and then read the contents of the parts
        """
        with ZipFile(self.path, "r") as zr:
            with zr.open(self.types.zipname, "r") as f:
                self.types.read(f)

            for zipname in zr.namelist():
                if zipname == self.types.zipname:
                    continue

                uri_str = Uri.zipname2str(zipname)
                part = self.add_part(uri_str, self.types.get_type(uri_str))
                with zr.open(zipname, "r") as f:
                    part.read(f)
        return self

    def write(self, path: Path) -> None:
        """Writes the package parts and content types to the given path

        :param path: path where package is to be written to.
        """
        with ZipFile(path, "w", compression=ZIP_DEFLATED) as zw:
            for part in self._parts.values():
                zipname = part.uri.zipname
                with zw.open(zipname, "w") as f:
                    part.write(f)

            with zw.open(self.types.zipname, "w") as f:
                self.types.write(f)

    def exists_part(self, uri_str: str) -> bool:
        """Checks if |part| exists in the |package|

        :param uri_str: uri string
        :returns: True | False
        """
        return uri_str in self._parts

    def add_part(self, uri_str: str, type_) -> Part:  # type: ignore[no-untyped-def]
        """Constructs a |part| or |relspart| object and add to the parts
        collection of the |package|. part or relspart is decided based on the
        uri_str value, if uri_str ends with .rels relspart is constructed
        otherwise part is constructed.

        If there is hook available for the given type then that is called
        after the part is constructed. the return value of the callback hook
        is assigned to the _typeobj of the part. It is callback hook's
        responsibility to keep the reference to the part object which is passed
        to the callback hook call.

        :param uri_str: string value of uri
        :param type_: type of the part object
        :returns: |part| object
        :exception ValueError: if part already exists with given uri_str
        """
        if self.exists_part(uri_str):
            raise ValueError("Part already exists with given uri")

        uri = Uri(uri_str)
        part_class = Part
        if uri.is_rels:
            part_class = RelsPart  # to have some specific methods for relspart

        part = part_class(self, uri_str, type_)
        self._parts[uri_str] = part

        if type_ in self._part_hooks:
            hook = self._part_hooks[type_]
            # connection between part object and the object per type
            part.typeobj = hook(part)

        return part

    def get_part(self, uri_str: str) -> Part | None:
        """Gets part having the given uri from the package

        :param uri_str: string value of the uri
        :returns: |part| object with given uri
        """
        if self.exists_part(uri_str):
            return self._parts[uri_str]
        return None

    def get_parts(self, type_: str) -> list[Part]:
        """Gets list of parts of the given content type

        :param type: content type of the part
        :returns: list of parts with the given type
        """
        return [part for part in self._parts.values() if part.type == type_]

    def register_part_hook(self, type_: str, callback: type[XmlTypeobjBase]) -> None:
        """Registers a callback hook to the content type.
        Hooks are called when part is created and before read method is called.
        Any existing hook on the given type will be over written

        :param type: content type of the part
        :param callback: callable (class or method or function) accepts one arg
        """
        self._part_hooks[type_] = callback

    def remove_part(self, uri_str: str) -> None:
        """Removes a |part| from the |package|. Also removes entry from types
        if the type is not refering to any other part.

        :param uri_str: string value of uri
        """
        if (part := self.get_part(uri_str)) is not None:
            type = part.type
            del self._parts[uri_str]
            if len(self.get_parts(type)) == 0:
                self._types.remove_type(uri_str)

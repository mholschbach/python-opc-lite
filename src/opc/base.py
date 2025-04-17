from abc import ABC

from lxml import etree

from .parser import Parser


class Base(ABC):
    """This is a abstract class that initializes and provide parent property

    Objects of a class that inherits this class gets parent property
    See |cp| for example

    :param parent: parent object that will be returned through parent property
    """

    def __init__(self, parent: object):
        self._parent = parent

    @property
    def parent(self) -> object:
        """Returns the parent object of current object"""
        return self._parent


class XmlBase:
    """This is a base class for objects that has xml content. It is inherited
    by classes like |ct|
    """

    _e: etree._Element | None

    def __init__(self) -> None:
        self._e = None
        self._parser = Parser()

    @property
    def e(self) -> etree._Element | None:
        """returns the underlying xml element object"""
        if self._e is not None:
            return self._e
        return None

    @e.setter
    def e(self, value: etree._Element) -> None:
        self._e = value

    @property
    def parser(self) -> Parser:
        """returns the parser object"""
        return self._parser

    def read(self, f) -> None:  # type: ignore[no-untyped-def]
        """parse the given file object as xml and assigns the root element to
        self._e
        """
        self._e = self._parser.parse(f).getroot()

    def write(self, f) -> None:  # type: ignore[no-untyped-def]
        """writes the xml content in self._e to the given file object. utf-8
        encoding, xml_declaration and standalone properties are applied to xml
        """
        if self._e is not None:
            f.write(
                etree.tostring(
                    self._e, encoding="UTF-8", xml_declaration=True, standalone=True
                )
            )


class PartBase:
    """This is a abstract class that part and relspart classes inherits

    Objects of a class that inherits this class gets package property
    See |part| for example

    """

    _parent: object

    @property
    def package(self) -> object:
        """property that returns the package object"""
        return self._parent


class XmlTypeobjBase(XmlBase, Base):
    """This is a base class for classes like
    |cp|. It inherits class :class:`opc.base.XmlBase` for xml related data
    and behavior. It also inherits class :class:`opc.base.Base`.

    :param part: |part| object
    """

    _part: object

    def __init__(self, part: object):
        XmlBase.__init__(self)
        Base.__init__(self, part)
        self._part = part

    @property
    def part(self) -> object:
        """property that returns the part object of say
        |cp| typeobj
        """
        return self._part

from datetime import datetime

from lxml import etree

from .base import Base, XmlTypeobjBase
from .datetime import Dt


class PropertyItem(Base):
    """class of property items of core property objects

    PropertyItem.dt_props are the datetime value properties.
    Others are string value properties

    :param parent: |cp| object. Needed to access the xml
    :param name: name of the property
    """

    dt_props = ["last print date", "creation date", "last save time"]
    """properties that are datetime related"""

    def __init__(self, parent: XmlTypeobjBase, name: str):
        super().__init__(parent)
        self._name = name

    @property
    def e(self) -> etree._Element:
        """Returns the xml element of the property item"""
        e = self.parent.e  # type: ignore[attr-defined]
        return e.find(e.qn(self.pfxname))

    @property
    def pfxname(self) -> str:
        """Returns the prefix name of the property item eg. 'dc:title'"""
        return self.parent.supported_properties[self._name]  # type: ignore[attr-defined]

    @property
    def Value(self) -> str | None:
        """Value of the property item

        :getter: Returns the value
        :setter: Sets the value
        :type: datetime.datetime for datetime related property, str for others

        Example::

            from datetime import datetime
            dt_now = datetime.now().astimezone()
            <core_properties>.Item('creation date').Value = dt_now
            <core_properties>.Item('author').Value = "New Author"
        """
        if self.e is not None and self.e.text is not None:
            if self._name in self.dt_props:
                return str(Dt.from_w3cdtf(self.e.text))
            return self.e.text
        return None

    @Value.setter
    def Value(self, newvalue: datetime) -> None:
        if self._name in self.dt_props and not isinstance(newvalue, datetime):
            raise TypeError("newvalue must be a datetime object for this property")
        if self.e is None:
            e = self.parent.e
            e.append(e.makeelement(e.qn(self.pfxname)))

        if isinstance(newvalue, datetime):
            self.e.text = Dt.to_w3cdtf(newvalue)
        else:
            self.e.text = newvalue


class CoreProperties(XmlTypeobjBase):
    """Object of this class is a collection of |package| core properties

    Supported properties are below:
        - title
        - subject
        - author
        - keywords
        - comments
        - last author
        - revision number
        - last print date
        - creation date
        - last save time
        - category
        - content status

    Of above following are datetime related properties others are strings
        - last print date
        - creation date
        - last save time

    Example::

        from datetime import datetime
        dt_now = datetime.now().astimezone()
        <core_properties>.Item('creation date').Value = dt_now
        <core_properties>.Item('author').Value = "New Author"

    """

    type = "application/vnd.openxmlformats-package.core-properties+xml"
    supported_properties = {
        "title": "dc:title",
        "subject": "dc:subject",
        "author": "dc:creator",
        "keywords": "cp:keywords",
        "comments": "dc:description",
        "last author": "cp:lastModifiedBy",
        "revision number": "cp:revision",
        "last print date": "cp:lastPrinted",
        "creation date": "dcterms:created",
        "last save time": "dcterms:modified",
        "category": "cp:category",
        "content status": "cp:contentStatus",
    }

    def Item(self, prop: str) -> PropertyItem:
        """returns the |pi| object from the given property name"""
        prop = prop.lower()
        if prop not in self.supported_properties:
            raise ValueError("Unsupported property")

        return PropertyItem(self, prop)

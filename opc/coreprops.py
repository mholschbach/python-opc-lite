from .base import XmlTypeobjBase, Base
from .datetime import dt
from datetime import datetime

class PropertyItem(Base):
    """class of property item. 
    PropertyItem.dt_props are the datetime value properties
    others are string value properties
    """
    dt_props = ['last print date', 'creation date', 'last save time']

    def __init__(self, parent, name):
        super().__init__(parent)
        self._name = name

    @property
    def e(self):
        """Returns the xml element of the object"""
        e = self.parent.e
        return e.find(e.qn(self.pfxname))
    
    @property
    def pfxname(self):
        """Returns the prefix name of the object eg. 'dc:title'"""
        return self.parent.supported_properties[self._name]


    @property
    def Value(self):
        """Returns the value i.e. string or datetime object depending on the object"""
        if self.e is not None:
            if self._name in self.dt_props:
                return dt.from_w3cdtf(self.e.text)
            return self.e.text

    @Value.setter
    def Value(self, newvalue):
        """sets the value of the object 
        Example:
        dt_now = datetime.now().astimezone()
        <core_properties>.Item('creation date').Value = dt_now
        <core_properties>.Item('author').Value = "New Author"
        """
        if self.e is None:
            e = self.parent.e
            e.append(e.makeelement(e.qn(self.pfxname)))
            
        if isinstance(newvalue, datetime):
            self.e.text = dt.to_w3cdtf(newvalue)
        else:
            self.e.text = newvalue



class CoreProperties(XmlTypeobjBase):
    """Object of this class is a collection of package core properties
    Supported properties are below:
        'title'
        'subject'
        'author'
        'keywords'
        'comments'
        'last author' 
        'revision number'
        'last print date'
        'creation date'
        'last save time'
        'category' 
        'content status'
    Examples:
    <core_properties>.Item('author').Value
    <core_properties>.Item('author').Value = 'New Author'

    Date time properties return the datetime object
    created_datetime = <core_properties>.Item('creation date').Value

    to set the 'last print date' 'creation date' 'last save time' pass datetime object
    dt_now = datetime.now().astimezone()
    <core_properties>.Item('creation date').Value = dt_now

    """
    type = "application/vnd.openxmlformats-package.core-properties+xml"
    supported_properties = {
        'title':'dc:title', 
        'subject':'dc:subject', 
        'author':'dc:creator', 
        'keywords':'cp:keywords', 
        'comments':'dc:description',
        'last author':'cp:lastModifiedBy', 
        'revision number':'cp:revision', 
        'last print date':'cp:lastPrinted', 
        'creation date':'dcterms:created', 
        'last save time':'dcterms:modified',
        'category':'cp:category', 
        'content status':'cp:contentStatus', 
    }
    
    def Item(self, prop):
        """returns the property item object from the given property name"""
        prop = prop.lower()
        if prop not in self.supported_properties:
            raise ValueError("Unsupported property")

        return PropertyItem(self, prop)

        

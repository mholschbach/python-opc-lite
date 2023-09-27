from lxml import etree
from unittest import mock
from opc.base import Base, PartBase, XmlTypeobjBase, XmlBase
from opc.parser import Parser

def test_base_parent():
    obj = object()
    base = Base(obj)
    assert base.parent is obj
    
def test_xmlbase_e(xmlbase_presentation):
    assert isinstance(xmlbase_presentation.e, etree.ElementBase)

def test_xmlbase_parser(xmlbase_presentation):
    assert isinstance(xmlbase_presentation.parser, Parser)

def test_xmlbase_read(presentation_xml_path, xmlbase):
    assert xmlbase.e is None
    with open(presentation_xml_path) as f:
        xmlbase.read(f)
    assert isinstance(xmlbase.e, etree.ElementBase)

def test_xmlbase_write(presentation_xml_path, xmlbase_presentation, tmp_path):
    with open(presentation_xml_path) as f:
        expected = etree.parse(f).getroot()

    path = tmp_path / "presentation.xml"
    with open(path, 'wb') as f:
        xmlbase_presentation.write(f)
    with open(path) as f:
        actual = etree.parse(f).getroot()
    assert etree.tostring(expected) == etree.tostring(actual)

def test_partbase_package_property_returns_package_object(package):
    for part in package._parts.values():
        assert isinstance(part, PartBase)
        assert part.package is package

def test_xmltypeobjbase_part_property():
    mock_part = mock.MagicMock()
    obj = XmlTypeobjBase(mock_part)
    assert obj.part is mock_part

def test_xmltypeobjbase_subclass_of_xmlbase_and_base():
    assert issubclass(XmlTypeobjBase, (XmlBase, Base))


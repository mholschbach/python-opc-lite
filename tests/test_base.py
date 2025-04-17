from pathlib import Path
from unittest import mock

from lxml import etree

from opc.base import Base, PartBase, XmlBase, XmlTypeobjBase
from opc.package import Package
from opc.parser import Parser


def test_base_parent() -> None:
    obj = object()
    base = Base(obj)
    assert base.parent is obj


def test_xmlbase_e(xmlbase_presentation: XmlBase) -> None:
    assert isinstance(xmlbase_presentation.e, etree.ElementBase)


def test_xmlbase_parser(xmlbase_presentation: XmlBase) -> None:
    assert isinstance(xmlbase_presentation.parser, Parser)


def test_xmlbase_read(presentation_xml_path: str, xmlbase: XmlBase) -> None:
    assert xmlbase.e is None
    with open(presentation_xml_path) as f:
        xmlbase.read(f)
    assert isinstance(xmlbase.e, etree.ElementBase)


def test_xmlbase_write(
    presentation_xml_path: str, xmlbase_presentation: XmlBase, tmp_path: Path
) -> None:
    with open(presentation_xml_path) as f:
        expected = etree.parse(f).getroot()

    path = tmp_path / "presentation.xml"
    with open(path, "wb") as f:
        xmlbase_presentation.write(f)
    with open(path) as f:
        actual = etree.parse(f).getroot()
    assert etree.tostring(expected) == etree.tostring(actual)


def test_partbase_package_property_returns_package_object(package: Package) -> None:
    for part in package._parts.values():
        assert isinstance(part, PartBase)
        assert part.package is package


def test_xmltypeobjbase_part_property() -> None:
    mock_part = mock.MagicMock()
    obj = XmlTypeobjBase(mock_part)
    assert obj.part is mock_part


def test_xmltypeobjbase_subclass_of_xmlbase_and_base() -> None:
    assert issubclass(XmlTypeobjBase, (XmlBase, Base))

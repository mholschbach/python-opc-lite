from pathlib import Path

import pytest

from opc import Package
from opc.base import XmlBase
from opc.parser import Parser
from opc.part import Part
from opc.types import Types


@pytest.fixture
def data_path() -> Path:
    return Path(__file__).parent / "data"


@pytest.fixture
def pptx_path(data_path: Path) -> Path:
    return data_path / "blank.pptx"


@pytest.fixture
def package(pptx_path: Path) -> Path:
    return Package(pptx_path).read()


@pytest.fixture
def types(package: Package) -> Types:
    return package.types


@pytest.fixture
def presentation_uri_str() -> str:
    return "/ppt/presentation.xml"


@pytest.fixture
def thumbnail_url_str() -> str:
    return "/docProps/thumbnail.jpeg"


@pytest.fixture
def presentation_type() -> str:
    return (
        "application/vnd.openxmlformats-officedocument.presentationml"
        ".presentation.main+xml"
    )


@pytest.fixture
def thumbnail_type() -> str:
    return "image/jpeg"


@pytest.fixture
def part() -> Part:
    return Part(None, "/some/uri.def", "http://some/default/type")


@pytest.fixture
def presentation_part(package: Package, presentation_uri_str: str) -> Part:
    return package.get_part(presentation_uri_str)


@pytest.fixture
def presentation_relspart(presentation_part):
    return presentation_part.get_rels_part()


@pytest.fixture
def presentation_relstypeobj(presentation_relspart):
    return presentation_relspart.typeobj


@pytest.fixture
def all_parts(package: Package):
    return package._parts.values()


@pytest.fixture
def slide_part(package: Package):
    return package.get_part("/ppt/slides/slide1.xml")


@pytest.fixture
def parser() -> Parser:
    return Parser()


@pytest.fixture
def presentation_xml_path(data_path: Path) -> Path:
    return data_path / "presentation.xml"


@pytest.fixture
def core_properties(package: Package):
    return package.core_properties


@pytest.fixture
def xmlbase_presentation(presentation_xml_path: str) -> XmlBase:
    x = XmlBase()
    with open(presentation_xml_path) as f:
        x.read(f)
    return x


@pytest.fixture
def xmlbase():
    return XmlBase()

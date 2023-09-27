import pytest
from pathlib import Path
from opc import Package
from opc.part import Part
from opc.parser import Parser
from opc.base import XmlBase

@pytest.fixture
def data_path():
    return Path(__file__).parent / "data"

@pytest.fixture
def pptx_path(data_path):
    return data_path / "blank.pptx"

@pytest.fixture
def package(pptx_path):
    return Package(pptx_path).read()

@pytest.fixture
def types(package):
    return package.types

@pytest.fixture
def presentation_uri_str():
    return '/ppt/presentation.xml'

@pytest.fixture
def thumbnail_url_str():
    return "/docProps/thumbnail.jpeg"

@pytest.fixture
def presentation_type():
    return "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"

@pytest.fixture
def thumbnail_type():
    return "image/jpeg"

@pytest.fixture
def part():
    return Part(None, "/some/uri.def", "http://some/default/type")


@pytest.fixture
def presentation_part(package, presentation_uri_str):
    return package.get_part(presentation_uri_str)

@pytest.fixture
def presentation_relspart(presentation_part):
    return presentation_part.get_rels_part()

@pytest.fixture
def presentation_relstypeobj(presentation_relspart):
    return presentation_relspart.typeobj

@pytest.fixture
def all_parts(package):
    return package._parts.values()

@pytest.fixture
def slide_part(package):
    return package.get_part('/ppt/slides/slide1.xml')

@pytest.fixture
def parser():
    return Parser()
    
@pytest.fixture
def presentation_xml_path(data_path):
    return data_path / "presentation.xml"

@pytest.fixture
def core_properties(package):
    return package.core_properties

@pytest.fixture
def xmlbase_presentation(presentation_xml_path):
    x = XmlBase()
    with open(presentation_xml_path) as f:
        x.read(f)
    return x

@pytest.fixture
def xmlbase():
    return XmlBase()
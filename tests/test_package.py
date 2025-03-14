from zipfile import ZipFile
from unittest import mock
import os
import pytest
from opc.types import Types
from opc.relspart import RelsPart
from opc.coreprops import CoreProperties
from opc.package import Package
from opc.part import Part


def test_package_path(package, pptx_path):
    assert package.path == pptx_path
    assert package.path.__class__ is pptx_path.__class__


def test_package_parts_count(package):
    assert len(package._parts) == 36


def test_package_types(package, types):
    assert package.types is types
    assert isinstance(package.types, Types)


def test_package_has_relspart_hook(package):
    assert RelsPart.type in package._part_hooks


def test_package_has_corepropspart_hook(package):
    assert CoreProperties.type in package._part_hooks


def test_package_read_all_items_count_tally(package):
    parts_count = len(package._parts)
    total_count = parts_count + 1  # add types
    with ZipFile(package.path, 'r') as zr:
        assert len(zr.namelist()) == total_count


def test_package_write_all_items_count_tally(package, data_path):
    filename = "package_write.pptx"
    path = data_path / filename
    if os.path.exists(path):
        os.remove(path)
    package.write(path)
    pkg = Package(path).read()
    os.remove(path)
    assert len(package._parts) == len(pkg._parts)


def test_package_exists_part(package):
    assert package.exists_part('/ppt/slides/slide1.xml')
    assert not package.exists_part('/ppt/slides/slide2.xml')


def test_package_add_part_error_if_part_exists_already(package,
                                                       presentation_part):
    with pytest.raises(ValueError):
        package.add_part(presentation_part.uri.str, None)


def test_package_add_part_class_of_part_used_is_part(package):
    part = package.add_part('/ppt/some/part.xml', None)
    assert isinstance(part, Part)


def test_package_add_part_class_of_part_used_is_relspart(package):
    part = package.add_part('/ppt/some/part.rels', None)
    assert isinstance(part, RelsPart)


def test_package_add_part_uri_is_added_to_parts(package):
    part = package.add_part('/ppt/some/part.xml', None)
    assert package.exists_part(part.uri.str)


def test_package_get_part_uri_match(package, presentation_uri_str):
    assert package.get_part(
        presentation_uri_str).uri.str == presentation_uri_str


def test_package_get_parts_no_part_with_type_none(package):
    assert len(package.get_parts(None)) == 0


def test_package_get_parts_with_rels_type_count(package,
                                                presentation_relspart):
    assert 15 == len(package.get_parts(presentation_relspart.type))


def test_package_register_part_hook_if_hook_used(package):
    mock_callback = mock.MagicMock()
    package.register_part_hook('/some/type', mock_callback)
    package.add_part('/some/uri.xml', '/some/type')
    assert mock_callback.assert_called_once


def test_package_remove_part(package, presentation_part):
    assert len(package.get_parts(presentation_part.type)) == 1
    package.remove_part(presentation_part.uri.str)
    assert not package.exists_part(presentation_part.uri.str)
    assert package.get_parts(presentation_part.type) == []


def test_package_remove_part_but_types_still_has_it(package,
                                                    presentation_relspart):
    before_count = len(package.get_parts(presentation_relspart.type))
    package.remove_part(presentation_relspart.uri.str)
    after_count = len(package.get_parts(presentation_relspart.type))
    assert before_count == after_count + 1

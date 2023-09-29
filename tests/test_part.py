from opc.package import Part
from opc.uri import Uri


def test_all_parts_are_instances_of_class(all_parts):
    for part in all_parts:
        assert isinstance(part, Part)


def test_all_parts_have_uri_property(all_parts):
    for part in all_parts:
        assert isinstance(part.uri, Uri)


def test_all_parts_have_type_property(all_parts):
    for part in all_parts:
        assert hasattr(part, "type")


def test_all_parts_have_typeobj_property(all_parts):
    for part in all_parts:
        assert hasattr(part, "typeobj")


def test_all_parts_have_read_method(all_parts):
    for part in all_parts:
        assert hasattr(part, "read") and callable(getattr(part, 'read'))


def test_all_parts_have_write_method(all_parts):
    for part in all_parts:
        assert hasattr(part, "write") and callable(getattr(part, 'write'))


def test_get_rels_part(presentation_part, presentation_relspart):
    assert presentation_relspart is presentation_part.get_rels_part()


def test_get_abs_uri_str(presentation_part, slide_part):
    assert presentation_part.get_abs_uri_str('slides/slide1.xml') == \
        slide_part.uri.str


def test_get_related_part(presentation_part, slide_part):
    assert slide_part is presentation_part.get_related_part('rId2')

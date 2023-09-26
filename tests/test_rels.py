import pytest
from opc.rels import Relationships

def test_typeobj_is_initialized_for_all_rels_parts(package):
    for part in package._parts.values():
        if part.uri.is_rels:
            assert isinstance(part.typeobj, Relationships)

@pytest.mark.parametrize("rid, expectation", [
    ("rId1", "slideMasters/slideMaster1.xml"),
    ("rId2", "slides/slide1.xml"),
    ("rId3", "presProps.xml"),
    ("rId4", "viewProps.xml"),
    ("rId5", "theme/theme1.xml"),
    ])
def test_get_target_rel_uri_str(presentation_relstypeobj, rid, expectation):
    assert expectation == presentation_relstypeobj.get_target_rel_uri_str(rid)


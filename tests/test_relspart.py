import pytest
from opc.relspart import RelsPart

def test_all_rels_parts_class(package):
    for part in package._parts.values():
        if part.uri.is_rels:
            assert isinstance(part, RelsPart)

@pytest.mark.parametrize("rid, expectation", [
    ("rId1", "slideMasters/slideMaster1.xml"),
    ("rId2", "slides/slide1.xml"),
    ("rId3", "presProps.xml"),
    ("rId4", "viewProps.xml"),
    ("rId5", "theme/theme1.xml"),
    ])
def test_get_target_rel_uri_str(presentation_relspart, rid, expectation):
    assert expectation == presentation_relspart.get_target_rel_uri_str(rid)









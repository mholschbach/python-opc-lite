import pytest


def test_zipname(types):
    assert types.zipname == "[Content_Types].xml"


@pytest.mark.parametrize("uri_str", ["presentation_uri_str", "thumbnail_url_str"])
def test_remove_type(types, uri_str, request):
    uri_str = request.getfixturevalue(uri_str)
    before_type = types.get_type(uri_str)
    types.remove_type(uri_str)
    assert before_type != types.get_type(uri_str)


@pytest.mark.parametrize(
    "uri_str,type",
    [
        ("presentation_uri_str", "presentation_type"),
        ("thumbnail_url_str", "thumbnail_type"),
    ],
)
def test_get_type(types, uri_str, type, request):
    uri_str = request.getfixturevalue(uri_str)
    type = request.getfixturevalue(type)
    assert type == types.get_type(uri_str)


def test_add_default(types, part):
    types.add_default(part)
    assert types.get_type(str(part.uri)) == part.type


def test_add_override(types, part):
    types.add_override(part)
    assert types.get_type(str(part.uri)) == part.type

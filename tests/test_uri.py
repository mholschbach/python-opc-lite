import pytest

from opc.uri import Uri


@pytest.fixture
def get_uri_presentation():
    return Uri("/ppt/presentation.xml")


@pytest.fixture(params=["/_rels/.rels", "/ppt/slides/_rels/slide1.xml.rels"])
def get_uri_rels(request):
    return Uri(request.param)


def test_uri_takes_only_str():
    with pytest.raises(TypeError):
        Uri(1)


def test_uri_str_starts_with_slash():
    with pytest.raises(ValueError):
        Uri("some/path")


def test_uri_str_value(get_uri_presentation):
    assert str(get_uri_presentation) == "/ppt/presentation.xml"


def test_uri_ext_value(get_uri_rels):
    assert get_uri_rels.ext == "rels"


def test_uri_zipname_value(get_uri_presentation):
    assert get_uri_presentation.zipname == "ppt/presentation.xml"


@pytest.mark.parametrize(
    "uri_str,expectation", [("/_rels/.rels", True), ("/docProps/core.xml", False)]
)
def test_uri_is_rels(uri_str, expectation):
    assert Uri(uri_str).is_rels == expectation


@pytest.mark.parametrize(
    "uri_str, expectation",
    [("/", "/_rels/.rels"), ("/docProps/core.xml", "/docProps/_rels/core.xml.rels")],
)
def test_uri_rels(uri_str, expectation):
    assert Uri(uri_str).rels == expectation


@pytest.mark.parametrize(
    "zipname, expectation",
    [("_rels/.rels", "/_rels/.rels"), ("docProps/core.xml", "/docProps/core.xml")],
)
def test_uri_zipname2str(zipname, expectation):
    assert Uri.zipname2str(zipname) == expectation


@pytest.mark.parametrize(
    "uri_str, rel_target_uri_str, expectation",
    [
        ("/ppt/presentation.xml", "slides/slide1.xml", "/ppt/slides/slide1.xml"),
        (
            "/ppt/slides/slide1.xml",
            "../slideLayouts/slideLayout1.xml",
            "/ppt/slideLayouts/slideLayout1.xml",
        ),
        (
            "/ppt/slides/slide1.xml",
            "../embeddings/Microsoft_Excel_Worksheet.xlsx",
            "/ppt/embeddings/Microsoft_Excel_Worksheet.xlsx",
        ),
        (
            "/ppt/handoutMasters/handoutMaster1.xml",
            "../theme/theme4.xml",
            "/ppt/theme/theme4.xml",
        ),
    ],
)
def test_uri_get_abs(uri_str, rel_target_uri_str, expectation):
    assert Uri(uri_str).get_abs(rel_target_uri_str) == expectation

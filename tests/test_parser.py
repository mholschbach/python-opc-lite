import pytest
from unittest import mock
from opc.parser import etree, ElementBase

def test_element_base_ns_of_no_namespace_element(parser):
    e = parser.makeelement('some')
    assert e.ns is None

def test_element_base_ns_of_no_namespace_element(parser):
    e = parser.makeelement('{somenamespace}some')
    assert e.ns == "somenamespace"
    
def test_element_base_qn_no_prefix_no_nsmap_and_e_has_no_nsmap(parser):
    e = parser.makeelement('some')
    assert e.qn('just') == 'just'

def test_element_base_qn_no_prefix_no_nsmap_and_e_has_nsmap(parser):
    e = parser.makeelement('some', nsmap={None:"somens"})
    assert e.qn('just') == '{somens}just'
    
def test_element_base_qn_no_prefix_empty_nsmap_and_e_has_nsmap(parser):
    e = parser.makeelement('some', nsmap={None:"somens"})
    assert e.qn('just', nsmap={}) == 'just'

def test_element_base_qn_no_prefix_none_in_nsmap_and_e_has_diff_ns_for_none(parser):
    e = parser.makeelement('some', nsmap={None:"somens"})
    assert e.qn('just', nsmap={None:"nsnone"}) == '{nsnone}just'
    
def test_element_base_qn_no_prefix_no_nsmap_no_none_in_e_nsmap(parser):
    e = parser.makeelement('{nssome}some')
    assert e.qn('just') == 'just'
    
def test_element_base_qn_with_prefix_no_nsmap_and_prefix_not_in_e_nsmap(parser):
    e = parser.makeelement('some', nsmap={None:"somens"})
    with pytest.raises(KeyError):
        e.qn('p:just')

def test_element_base_qn_with_prefix_no_nsmap_and_prefix_in_e_nsmap(parser):
    e = parser.makeelement('some', nsmap={"p":"somens"})
    assert e.qn('p:just') == "{somens}just"

def test_element_base_qn_with_prefix_with_nsmap_but_prefix_absent_and_prefix_in_e_nsmap(parser):
    e = parser.makeelement('some', nsmap={"p":"somens"})
    with pytest.raises(KeyError):
        e.qn('p:just', nsmap={'q':"qnamespace"})

def test_element_base_qn_with_prefix_with_nsmap_prefix_present(parser):
    e = parser.makeelement('some', )
    e.qn('p:just', nsmap={'p':"pnamespace"}) == "{pnamespace}just"

def test_element_base_makeelement(parser):
    e = parser.makeelement('some', )
    e2 = e.makeelement('somelem')
    assert isinstance(e2, e.__class__)

def test_element_base_dump(parser):
    e = parser.makeelement('some')
    etree.dump = mock.MagicMock()
    e.dump()
    etree.dump.assert_called_once_with(e)

def test_parser(parser):
    assert isinstance(parser.makeelement('some'), ElementBase)

def test_parser_parse(parser, presentation_xml_path):
    e = parser.parse(presentation_xml_path)
    for e in e.getroot():
        assert isinstance(e, ElementBase)


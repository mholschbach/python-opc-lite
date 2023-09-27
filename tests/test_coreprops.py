import pytest
from contextlib import nullcontext as does_not_raise
from opc.coreprops import CoreProperties, PropertyItem
from opc.parser import ElementBase

def test_coreprops_raise_valueerror_for_unsupported_properties(core_properties):
    with pytest.raises(ValueError):
        core_properties.Item("un supported")

def test_coreprops_item_returns_propertyitem_object(core_properties):
    assert isinstance(core_properties.Item("title"), PropertyItem)

def test_coreprops_item_returns_propertyitem_value(core_properties):
    assert core_properties.Item("title").Value == "PowerPoint Presentation"

def test_coreprops_item_returns_propertyitem_value_change(core_properties):
    new_title = "Changed title"
    core_properties.Item("title").Value = new_title
    assert core_properties.Item("title").Value == new_title

def test_coreprops_supported_properties_do_not_raise_error(core_properties):
    with does_not_raise() as no_error:
        for prop in core_properties.supported_properties:
            core_properties.Item(prop).Value

def test_coreprops_value_of_prop_absent_in_xml_is_none(core_properties):
    assert None is core_properties.Item('comments').Value

def test_property_item_property_e_is_object_of_element_base(core_properties):
    assert isinstance(core_properties.Item('title').e, ElementBase)

@pytest.mark.parametrize("name, pfxname", [
    ('title','dc:title'),
    ('subject','dc:subject'),
    ('author','dc:creator'),
    ('keywords','cp:keywords'),
    ('comments','dc:description'),
    ('last author','cp:lastModifiedBy'),
    ('revision number','cp:revision'),
    ('last print date','cp:lastPrinted'),
    ('creation date','dcterms:created'),
    ('last save time','dcterms:modified'),
    ('category','cp:category'),
    ('content status','cp:contentStatus'),
])
def test_property_item_pfxname_values(core_properties, name, pfxname):
    assert core_properties.Item(name).pfxname == pfxname

def test_property_item_raises_error_if_non_datetime_object_given_for_datetime_props(core_properties):
    with pytest.raises(TypeError):
        for prop in PropertyItem.dt_props:
            core_properties.Item(prop).Value = ""



import pytest
from opc.coreprops import CoreProperties, PropertyItem


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










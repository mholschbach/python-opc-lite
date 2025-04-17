from lxml import etree

from .base import XmlTypeobjBase
from .parser import Parser


class Relationships(XmlTypeobjBase):
    """Class for object that represents the xml of |relspart| of the package.
    Inherits XmlTypeobjBase class. Xml of rels part is available as self.e
    """

    e: etree._Element
    xmlns = "http://schemas.openxmlformats.org/package/2006/relationships"

    def get_target_rel_uri_str(self, rid: str) -> str | None:
        """Method to get the target value of a relation given by rid

        :param rid: relation id string value
        :returns: string value of relationship's target value in xml

        Example::

            presentation_relspart = presentation_part.get_rels_part()
            relationships = presentation_relspart.typeobj

            # say the relationship xml is as below
            # <Relationship Id="rId2" Target="slides/slide1.xml" Type="..." />

            print(relationships.get_target_rel_uri_str('rId2'))
            # slides/slide1.xml
        """
        for r in self.e:
            if r.get("Id") == rid:
                return r.get("Target")
        return None

    def get_lst_target_rel_uri_str(self, reltype: str) -> list[str | None]:
        """Gets the list of relative uri of the target related by the given
        reltype

        :param reltype: str value
        :returns: list of Target attribute values of parts related by reltype
        """
        lst = []
        for r in self.e:
            if r.get("Type") == reltype:
                lst.append(r.get("Target"))
        return lst

    def init_e(self) -> None:
        """Add Relationships xml to the self.part object"""
        parser = Parser()
        self.e = parser.makeelement("Relationships", nsmap={None: self.xmlns})

    def add_relation(
        self, type: str, target: str, target_mode: str | None = None
    ) -> str:
        """Adds Relationships element to the xml. Assigns new Id and sets the
        Type, Target, TargetMode attributes to the element.

        :param type: str value of reltype
        :param target: relative uri str value of the part target wrt to part
            of this relspart object
        :param target_mode: optional param. Default value is None. No attribute
            TargetMode sets to the Relationships element if it is None. The
            value passed must be str type
        :returns: str value of the new id assigned to the element
        """

        parser = Parser()
        id = self.get_next_id()
        attrib = {"Id": id, "Type": type, "Target": target}
        if target_mode:
            attrib["TargetMode"] = target_mode
        rel = parser.makeelement(
            "Relationship", attrib=attrib, nsmap={None: self.xmlns}
        )
        self.e.append(rel)
        return id

    def get_next_id(self) -> str:
        """Returns the new available id for the new relationship element
        :returns: str value of the new available id
        """
        used = 0
        for r in self.e:
            if (id_string := r.get("Id")) is not None:
                id = int(id_string.replace("rId", ""))
                if id > used:
                    used = id
        return "rId" + str(used + 1)

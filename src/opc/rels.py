from .base import XmlTypeobjBase


class Relationships(XmlTypeobjBase):
    """Class for object that represents the xml of |relspart| of the package.
    Inherits XmlTypeobjBase class. Xml of rels part is available as self.e
    """

    def get_target_rel_uri_str(self, rid):
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
            if r.get('Id') == rid:
                return r.get('Target')

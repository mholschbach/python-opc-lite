from .base import XmlTypeobjBase
from .parser import Parser


class Relationships(XmlTypeobjBase):
    """Class for object that represents the xml of |relspart| of the package.
    Inherits XmlTypeobjBase class. Xml of rels part is available as self.e
    """
    xmlns = "http://schemas.openxmlformats.org/package/2006/relationships"

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

    def get_lst_target_rel_uri_str(self, reltype):
        lst = []
        for r in self.e:
            if r.get('Type') == reltype:
                lst.append(r.get('Target'))
        return lst

    def init_e(self):
        parser = Parser()
        self.e = parser.makeelement('Relationships', nsmap={None: self.xmlns})

    def add_relation(self, type, target, target_mode=None):
        parser = Parser()
        id = self.get_next_id()
        attrib = {'Id': id, 'Type': type, 'Target': target}
        if target_mode:
            attrib['TargetMode'] = target_mode
        rel = parser.makeelement(
            'Relationship', attrib=attrib, nsmap={None: self.xmlns})
        self.e.append(rel)
        return id

    def get_next_id(self):
        used = 0
        for r in self.e:
            id = int(r.get('Id').replace('rId', ''))
            if id > used:
                used = id
        return 'rId'+str(used + 1)

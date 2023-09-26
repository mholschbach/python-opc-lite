from .base import XmlTypeobjBase

class Relationships(XmlTypeobjBase):
    """A Typeobj class for rels part. Xml of rels part is available as self.e from its object"""
    
    def get_target_rel_uri_str(self, rid):
        """Returns the target relative uri string value from the given rid"""
        for r in self.e:
            if r.get('Id') == rid:
                return r.get('Target')


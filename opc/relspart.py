from .part import Part

class RelsPart(Part):
    """Class of part objects that are of type rels"""
    type = "application/vnd.openxmlformats-package.relationships+xml"
    
    def get_target_rel_uri_str(self, rid):
        """returns the target parts relative uri string value from given rid"""
        return self.typeobj.get_target_rel_uri_str(rid)

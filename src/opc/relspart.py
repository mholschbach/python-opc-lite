from .part import Part


class RelsPart(Part):
    """Class of part objects that are of type rels. Inherits the |part| class
    """
    type = "application/vnd.openxmlformats-package.relationships+xml"

    def get_target_rel_uri_str(self, rid):
        """gets the target value for the relatioship with id as given rid

        :param rid: relation id string value
        :returns: string value of relationship's target value in xml
        """
        return self.typeobj.get_target_rel_uri_str(rid)

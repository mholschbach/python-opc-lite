from pathlib import PurePosixPath, Path

class Uri():
    def __init__(self, uri_str):
        """given uri string value is stored """
        if not isinstance(uri_str, str):
            raise TypeError("uri_str must be str object")
        if not uri_str.startswith('/'):
            raise ValueError("uri_str must start with slash")
        self._uri_str = uri_str

    @property
    def str(self):
        """returns the string value of the uri"""
        return self._uri_str
    
    @property
    def ext(self):
        """returns the extension value of the uri"""
        return self.str.split('.')[-1]
    
    @property
    def zipname(self):
        """returns the zipname of the uri i.e. name valid for zipfile"""
        return self.str[1:]
    
    @property
    def is_rels(self):
        """returns if the uri is of a rels part or not"""
        return self.str.endswith('.rels')
    
    @property
    def rels(self):
        """returns the uri string of the rels part of the part this uri belongs to"""
        p = PurePosixPath(self.str)
        return str(p.parent / '_rels' / (p.name + '.rels'))
    
    @staticmethod
    def zipname2str(zipname):
        """returns uri string value from the given zipname"""
        return '/'+zipname
    
    def get_abs(self, rel_target_uri_str):
        """returns the absolute uri string value from the given relative target value w.r.t the current part"""
        return '/' + str(((Path(self.str).parent / Path(rel_target_uri_str)).resolve().relative_to(Path('/').resolve())).as_posix() )
        
    
    
    

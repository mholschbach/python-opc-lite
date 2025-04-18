from os import path
from pathlib import Path, PurePosixPath


class Uri:
    """Class for uri of the |part| in a |package|.

    :param uri_str: string value of the part's uri
    """

    def __init__(self, uri_str: str) -> None:
        """initializes the attributes and checks for the input correctness"""
        if not isinstance(uri_str, str):
            raise TypeError("uri_str must be str object")
        if not uri_str.startswith("/"):
            raise ValueError("uri_str must start with slash")
        self._uri_str = uri_str

    @property
    def ext(self) -> str:
        """Readonly property.
        :returns: string extension value of the uri"""
        return self._uri_str.split(".")[-1]

    @property
    def zipname(self) -> str:
        """Readonly property.
        :returns: the zipname of the uri i.e. name valid for zipfile"""
        return self._uri_str[1:]

    @property
    def is_rels(self) -> bool:
        """Readonly property.
        :returns: boolean if the uri is of a rels part or not"""
        return self._uri_str.endswith(".rels")

    @property
    def rels(self) -> str:
        """Readonly property.
        :returns: the uri string of the |relspart| of current uri's part
        """
        p = PurePosixPath(self._uri_str)
        return str(p.parent / "_rels" / (p.name + ".rels"))

    @staticmethod
    def zipname2str(zipname: str) -> str:
        """static method.

        :param zipname: string value of the any zipname
        :returns: uri string value from the given zipname
        """
        return "/" + zipname

    def get_abs(self, rel_target_uri_str: str) -> str:
        """Method to get the absolute uri from the relative uri

        :param rel_target_uri_str: relative uri with respect to current uri
        :returns: absolute uri string value
        """
        return "/" + str(
            (
                (Path(self._uri_str).parent / Path(rel_target_uri_str))
                .resolve()
                .relative_to(Path("/").resolve())
            ).as_posix()
        )

    def get_rel(self, abs_target_uri_str: str) -> str:
        """Returns the relative uri str value from the given absolute uri str
        of the target part. Relative with respect to the current uri

        :param abs_target_uri_str: absolute uri str of target part
        :returns: str value of the relative uri
        """
        return Path(
            path.relpath(abs_target_uri_str, Path(self._uri_str).parent.as_posix())
        ).as_posix()

    def __str__(self) -> str:
        return self._uri_str

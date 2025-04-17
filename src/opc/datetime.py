from datetime import datetime as _datetime
from datetime import timezone as _timezone


class Dt:
    """A utility class providing static methods for datetime conversions
    related to w3cdtf format. w3cdtf format is like 2023-09-26T15:01:32Z in utc
    """

    @staticmethod
    def to_w3cdtf(dt_obj: _datetime) -> str:
        """Method to convert datetime object to w3cdtf format string value

        :param dt_obj: timezone aware datetime.datetime object
        :returns: str value of dt_obj in w3cdtf format
        """
        dt_obj = dt_obj.astimezone(_timezone.utc)
        string = _datetime.isoformat(dt_obj, timespec="seconds").replace("+00:00", "Z")
        return string if string.endswith("Z") else string + "Z"

    @staticmethod
    def from_w3cdtf(string: str) -> _datetime:
        """Method to convert w3cdtf format string to datetime.datetime object

        :param string: str value of datetime.datetime object in w3cdtf format
        :returns: datetime.datetime object
        """
        return _datetime.fromisoformat(string)

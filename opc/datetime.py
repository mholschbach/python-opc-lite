from datetime import datetime as _datetime, timezone as _timezone

class dt():

    @staticmethod
    def to_w3cdtf(dt_obj):
        """static method to convert datetime object to w3cdtf format string value"""
        dt_obj = dt_obj.astimezone(_timezone.utc)
        string = _datetime.isoformat(dt_obj, timespec="seconds").replace('+00:00', 'Z')
        return string if string.endswith('Z') else string+'Z'
    
    @staticmethod
    def from_w3cdtf(string):
        """static method to convert the w3cdtf format string value to datetime object"""
        return _datetime.fromisoformat(string)


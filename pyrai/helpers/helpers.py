import datetime

def to_rfc3339(dt):
    """
    Converts datetime objects to RFC3339 string for use with the API.

    Args:
        dt (datetime.datetime): A datetime.datetime object.

    Returns:
        string: An RFC3339 representation of dt.
    """
    return dt.astimezone(datetime.timezone.utc).isoformat()[:-6] + "Z"
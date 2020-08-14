import datetime
import urllib.parse

def to_rfc3339(dt):
    """
    Converts datetime objects to RFC3339 string for use with the API.

    Args:
        dt (datetime.datetime): A datetime.datetime object.

    Returns:
        string: An RFC3339 representation of dt.
    """
    return dt.astimezone(datetime.timezone.utc).isoformat()[:-6] + "Z"

def build_url(self, endpoint):
    """
    Builds a URL given an endpoint

    Args:
        endpoint (Endpoint: str): The endpoint to build the URL for 

    Returns:
        str: The URL to access the given API endpoint
    """

    return urllib.parse.urljoin(self.base_url, endpoint)
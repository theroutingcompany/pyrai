import IPython
from dateutil.parser import isoparse
from pyrai.helpers import to_rfc3339

def visualize(self, start_time=None, end_time=None):
    """
    Visualizes the fleet for the given time frame.

    Args:
        start_time (datetime.datetime or str): The start time, either as a datetime.datetime object or an ISO string. Set to the python fleet creation time if not set. Defaults to None.
        end_time (datetime.datetime or str): The end time, either as a datetime.datetime object or an ISO string. Set to the latest API call time if not set. Defaults to None.

    Returns:
        IFrame: A graphic view of the fleet through time.
    """
    if start_time is None:
        start_time = self.start_time
    
    if end_time is None:
        end_time = self.end_time

    if isinstance(start_time, str):
        start_time = isoparse(start_time)

    if isinstance(end_time, str):
        end_time = isoparse(end_time)

    url = self.vis_url.format( 
        start = to_rfc3339(start_time), 
        end = to_rfc3339(end_time), 
        api_key = self.api_key, 
        fleet_key = self.fleet_key)

    print(url)

    return IPython.display.IFrame(url, 800, 800)
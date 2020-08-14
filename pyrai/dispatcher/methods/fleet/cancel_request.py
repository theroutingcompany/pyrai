from pyrai.dispatcher.structures import Endpoints, StatusResponse, StatusError
import datetime
import requests
import json
from pyrai.helpers import to_rfc3339

def cancel_request(self, rid, event_time=None):
    """
    Attempts to cancel a request.

    Args:
        rid (int): The unique request ID
        event_time (datetime.datetime, optional): Time of the cancellation. Set to datetime.datetime.now() if not provided. Defaults to None.

    Raises:
        StatusError: If unsuccessful.

    Returns:
        Status Response: If the request is sucessfully cancelled.
    """
    if event_time is None:
        event_time = datetime.datetime.now()

    if event_time > self.end_time:
        self.end_time = event_time

    url = self.build_url(Endpoints.CANCEL_REQUEST)
    payload = {
        'id': rid,
        'event_time': to_rfc3339(event_time),
        'user_key': self.user_key.todict()
    }

    r = requests.post(url, data = json.dumps(payload))
    resp = r.json()
    
    if r.status_code == 200:
        return StatusResponse(resp=resp)
    else:
        raise StatusError(resp=resp)
from pyrai.dispatcher.structures.endpoints import Endpoints
from pyrai.dispatcher.structures.status_response import StatusResponse
from pyrai.dispatcher.structures.status_error import StatusError
import datetime
import requests
import json
from pyrai.helpers import to_rfc3339

def add_request(self, rid, pickup, dropoff, load, request_time=None):
    """
    Attempts to add a request.

    Args:
        rid (int): The unique request ID.
        pickup (Location): The pickup location.
        dropoff (Location): The dropoff location.
        load (int): The load (number of passengers).
        request_time (datetime.datetime, optional): Time of the request. This may be in the future for scheduled pickups. Set to datetime.datetime.now() if not provided. Defaults to None.

    Returns:
        StatusResponse: If successful.

    Raises:
        StatusError: If unsuccessful.
    """
    
    if request_time is None:
        request_time = datetime.datetime.now()

    if request_time > self.end_time:
        self.end_time = request_time

    url = self.build_url(Endpoints.ADD_REQUEST)
    payload = {
        'id': rid,
        'pickup': pickup.todict(),
        'dropoff': dropoff.todict(),
        'load': load,
        'request_time': to_rfc3339(request_time),
        'user_key': self.user_key.todict()
    }

    r = requests.post(url, data=json.dumps(payload))
    resp = r.json()

    if r.status_code == 200:
        return StatusResponse(resp=resp)
    else:
        raise StatusError(resp=resp)

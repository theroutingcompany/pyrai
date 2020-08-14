import requests
import datetime
import json
from pyrai.dispatcher.structures.endpoints import Endpoints
from pyrai.dispatcher.structures.status_response import StatusResponse
from pyrai.dispatcher.structures.status_error import StatusError

def make_vehicle_online(self, vid, location, capacity):
    """
    Attempts to make vehicle online.

    Args:
        vid (int): The vehicle ID.
        location (Location): The vehicle location.
        capacity (int): The vehicle capacity.

    Raises:
        StatusError: If unsuccessful.

    Returns:
        StatusReponse: If successful.
    """

    if datetime.datetime.now() > self.end_time:
        self.end_time = datetime.datetime.now()

    url = self.build_url(Endpoints.MAKE_VEHICLE_ONLINE)
    payload = {
        "location": location.todict(),
        "id": vid,
        'capacity': capacity,
        'user_key': self.user_key.todict()
    }
    r = requests.post(url, data=json.dumps(payload))
    resp = r.json()

    if r.status_code == 200:
        return StatusResponse(resp=resp)
    else:
        raise StatusError(resp=resp)
import requests
import datetime
import json
from pyrai.dispatcher.structures.endpoints import Endpoints
from pyrai.dispatcher.structures.status_response import StatusResponse
from pyrai.dispatcher.structures.status_error import StatusError

def make_vehicle_offline(self, vid, location):
    """
    Attempts to take vehicle offline.

    Args:
        vid (int): The vehicle ID.
        location (Location): The vehicle location.

    Raises:
        StatusError: If unsuccessful.

    Returns:
        StatusReponse: If successful.
    """
    if datetime.datetime.now() > self.end_time:
        self.end_time = datetime.datetime.now()

    url = self.build_url(Endpoints.MAKE_VEHICLE_OFFLINE)
    payload = {
        'location': location.todict(),
        'id': vid,
        'user_key': self.user_key.todict()
    }
    r = requests.post(url, data = json.dumps(payload))
    resp = r.json()
    
    if r.status_code == 200:
        return StatusResponse(resp=resp)
    else:
        raise StatusError(resp=resp)
import datetime
import requests
import json
from pyrai.dispatcher.structures.endpoints import Endpoints
from pyrai.dispatcher.structures.status_error import StatusError

def remove_vehicle(self, vid, location):
    """
    Attempts to remove a vehicle.

    Args:
        vid (int): The unique vehicle ID.
        location (Location): The vehicle Location.

    Returns:
        list[int]: If vehicle is successfully removed, returns
            a list of IDs of passengers of the vehicle.

    Raises:
        StatusError: If unsuccessful.
    """

    if datetime.datetime.now() > self.end_time:
        self.end_time = datetime.datetime.now()
    
    url = self.build_url(Endpoints.REMOVE_VEHICLE)
    payload = {
        'location': location.todict(),
        'id': vid,
        'user_key': self.user_key.todict()
    }
    r = requests.post(url, data = json.dumps(payload))
    resp = r.json()

    if r.status_code == 200:
        if resp is not None:
            return resp.get('req_ids')
        else:
            return []
    else:
        raise StatusError(resp = resp)
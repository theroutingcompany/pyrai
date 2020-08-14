import requests
import json
from pyrai.dispatcher.structures.endpoints import Endpoints 
from pyrai.dispatcher.structures.vehicle import Vehicle
from pyrai.dispatcher.structures.status_error import StatusError


def get_vehicle_info(self, vid):
    """
    Attempts to get vehicle info.

    Args:
        vid (int): The unique vehicle ID.

    Raises:
        StatusError: If unsuccessful.

    Returns:
        Vehicle: If succesful, returns a vehicle object corresponding to the
            vehicle with ID vid.
    """
    url = self.build_url(Endpoints.GET_VEHICLE_INFO)
    params = {
        'api_key': self.api_key,
        'fleet_key': self.fleet_key,
        'id': vid
    }
    r = requests.get(url, params=params)
    resp = r.json()

    if r.status_code == 200:
        return Vehicle.fromdict(self, resp)
    else:
        raise StatusError(resp=resp)
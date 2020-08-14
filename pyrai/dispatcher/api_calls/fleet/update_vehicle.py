import datetime
import json
import requests
from pyrai.dispatcher.structures import Defaults, FleetParams, Endpoints, StatusError, Vehicle
from pyrai.helpers import to_rfc3339

def update_vehicle(self, vid, location, event, direction=Defaults.DEFAULT_DIRECTION, event_time=None, req_id=None):
    """
    Attempts to update a vehicle.

    Args:
        vid (int): The unique vehicle ID
        location (Location): The vehicle location.
        direction (float): Angle in radians clockwise away from true north
        event (VehicleEvent): Describes the current event for the vehicle. 
            pickup occurs when the vehicle has picked up a request. 
            dropoff occurs when the vehicle has dropped of a request. 
            progress should be set when the vehicle is moving to service a request, 
            either picking up or dropping off. The vehicle should be marked as 
            unassigned when it is is not assigned to any requests.
        event_time (datetime.datetime, optional): Time at which the vehicle update has occurred. 
            Set to datetime.datetime.now() if not provided. Defaults to None.
        req_id (int, optional): The unique ID of request the vehicle is servicing. 
            If the vehicle is unassigned, this may be omitted. Defaults to None.

    Returns:
        Vehicle: If successful.

    Raises:
        StatusError: If unsucessful.
    """
    if event_time is None:
        event_time = datetime.datetime.now()

    if event_time > self.end_time:
        self.end_time = event_time

    url = self.build_url(Endpoints.UPDATE_VEHICLE)
    payload = {
        'id': vid,
        'location': location.todict(),
        'direction': direction,
        'event_time': to_rfc3339(event_time),
        'event': event,
        'user_key': self.user_key.todict()
    }
    
    if req_id is not None:
        payload['req_id'] = req_id
    
    r = requests.post(url, data = json.dumps(payload))
    resp = r.json()

    if r.status_code == 200:
        return Vehicle.fromdict(self, resp)
    else:
        raise StatusError(resp = resp)
from pyrai.dispatcher.structures import Endpoints, VehicleAssignments, Vehicle, Request, Notification, StatusError
import datetime
import requests
from pyrai.helpers import to_rfc3339

def get_assignments(self, current_time=None):
    """
    Computes vehicle assignments for the fleet in the current state.

    Args:
        current_time (datetime.datetime, optional): Current time. Set to datetime.datetime.now() if not provided. Defaults to None.

    Raises:
        StatusError: If unsuccessful.

    Returns:
        VehicleAssignments: If assignments are successfully computed.
    """
    if current_time is None:
        current_time = datetime.datetime.now()

    if current_time > self.end_time:
        self.end_time = current_time

    url = self.build_url(Endpoints.COMPUTE_ASSIGNMENTS)
    payload = {
        'api_key': self.api_key,
        'fleet_key': self.fleet_key,
        'current_time': to_rfc3339(current_time)
    }

    r = requests.get(url, params=payload)
    resp = r.json()

    if r.status_code == 200:
        return VehicleAssignments(
            vehs=[Vehicle.fromdict(self, veh) for veh in resp.get('vehs')],
            requests=[Request.fromdict(self, req) for req in resp.get('reqs')],
            notifications=[Notification.fromdict(notif) for notif in resp.get('notifications')],
        )
    else:
        raise StatusError(resp = resp)
import datetime
from dateutil.parser import isoparse
from pyrai.dispatcher.structures.endpoints import Endpoints 
from pyrai.dispatcher.structures.vehicle_assignments import VehicleAssignments
from pyrai.dispatcher.structures.vehicle import Vehicle
from pyrai.dispatcher.structures.request import Request 
from pyrai.dispatcher.structures.notification import Notification
from pyrai.dispatcher.structures.status_error import StatusError
import requests
import json
from pyrai.helpers import to_rfc3339
from pytimeparse.timeparse import timeparse

def forward_simulate(self, duration, current_time=None):
    """
    Forward simulates the fleet for a given duration.

    Args:
        duration (string): A duration to forward simulate for, e.g. "5m."
        current_time (datetime.datetime or str, optional): The current time, from when the simulation will begin. Can be provided as a datetime.datetime object or ISO string. Set to datetime.datetime.now() if not provided. Defaults to None.

    Returns:
        VehicleAssignments: The final state of all vehicles and requests, after the simulation.

    Raises:
        StatusError: If unsuccessful.
    """
    if current_time is None:
        current_time = datetime.datetime.now()

    if isinstance(current_time, str):
        current_time = isoparse(current_time)

    duration_td = datetime.timedelta(seconds=timeparse(duration))

    if current_time + duration_td > self.end_time:
        self.end_time = current_time + duration_td

    url = self.build_url(Endpoints.FORWARD_SIMULATE)
    payload = {
        'user_key': self.user_key.todict(),
        'sim_duration': duration,
        'current_time': to_rfc3339(current_time)
    }

    r = requests.post(url, data = json.dumps(payload))
    resp = r.json()

    if r.status_code == 200:
        return VehicleAssignments(
            vehs=[Vehicle.fromdict(self, veh) for veh in resp.get('vehs')],
            requests=[Request.fromdict(self, req) for req in resp.get('reqs')],
            notifications=[Notification.fromdict(notif) for notif in resp.get('notifications')],
        )
    else:
        raise StatusError(resp = resp)
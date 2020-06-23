import datetime
import requests
from .status_response import *
from .structures import *

class ComputeAssignmentsQuery():
    def __init__(self, api_key, fleet_key, current_time = None):
        self.api_key = api_key
        self.fleet_key = fleet_key
        self.current_time = current_time

    def run(self):
        params = {'api_key': self.api_key,\
            'fleet_key': self.fleet_key}
        if self.current_time:
            params['current_time'] = self.current_time.astimezone(datetime.timezone.utc).isoformat()
        r = requests.get('http://api.routable.ai/dispatcher/assignments', params = params)
        if r.status_code == 200:
            return ComputeVehicleAssignmentsResponse(\
                [Vehicle.fromdict(veh) for veh in r.json().get('vehs')],\
                [Request.fromdict(req) for req in r.json().get('reqs')],\
                [Notification.fromdict(notif) for notif in r.json().get('notifications')],\
            )
        else:
            return StatusResponse(status = r.json().get('status'),\
            error = r.json().get('error'))
            

class ComputeVehicleAssignmentsResponse():
    def __init__(self, vehs, requests, notifications):
        self.vehs = vehs
        self.requests = requests
        self.notifications = notifications
    
    def __str__(self):
        return str(self.__dict__)
import requests
from .structures import *
from .status_response import *

class GetVehicleInfoQuery():
    def __init__(self, api_key, fleet_key, id):
        self.api_key = api_key
        self.fleet_key = fleet_key
        self.id = id

    def run(self):
        params = {'api_key': self.api_key,\
            'fleet_key': self.fleet_key,\
            'id': self.id}
        r = requests.get('http://api.routable.ai/dispatcher/vehicle', params = params)
        if r.status_code == 200:
            return Vehicle.fromdict(r.json())
        else:
            return StatusResponse(status = r.json().get('status'),\
                error = r.json().get('error'))        


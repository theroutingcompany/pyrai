import requests
import json
from .status_response import *

class CreateSimulatedFleetQuery():
    def __init__(self, api_key, params):
        self.api_key = api_key
        self.params = params

    def run(self):
        payload = {'api_key': self.api_key,\
            'params': self.params.__dict__}
        r = requests.post('http://api.routable.ai/dispatcher/simulation/create', data = json.dumps(payload))
        if r.status_code == 200:
            return CreateSimulatedFleetResponse(r.json().get('fleet_key'))
        else:
            return StatusResponse(status = r.json().get('status'),\
                error = r.json().get('error'))

class CreateSimulatedFleetResponse():
    def __init__(self, fleet_key):
        self.fleet_key = fleet_key

    def __str__(self):
        return str(self.__dict__)
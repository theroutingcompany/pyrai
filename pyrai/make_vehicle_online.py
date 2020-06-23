import requests
import json
from .status_response import *

class MakeVehicleOnlineQuery():
    def __init__(self, location, id, capacity, user_key):
        self.location = location
        self.id = id
        self.capacity = capacity
        self.user_key = user_key

    def run(self):
        payload = {'location': self.location.__dict__,\
            'id': self.id,\
            'capacity': self.capacity,\
            'user_key': self.user_key.__dict__}
        r = requests.post('http://api.routable.ai/dispatcher/vehicle/online',\
            data = json.dumps(payload))
        return StatusResponse(status = r.json().get('status'),\
            error = r.json().get('error'))
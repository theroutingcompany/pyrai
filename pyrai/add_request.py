import requests
import datetime
import json
from .status_response import *

class AddRequestQuery():
    def __init__(self, id, pickup, dropoff, load, request_time, user_key):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        self.load = load
        self.request_time = request_time
        self.user_key = user_key
    
    def run(self):
        payload = {'id': self.id,\
            'pickup': self.pickup.__dict__,\
            'dropoff': self.dropoff.__dict__,\
            'load': self.load,\
            'request_time': self.request_time.astimezone(datetime.timezone.utc).isoformat(),\
            'user_key': self.user_key.__dict__}
        r = requests.post('http://api.routable.ai/dispatcher/request/add', data = json.dumps(payload))
        return StatusResponse(status = r.json().get('status'),\
            error = r.json().get('error'))


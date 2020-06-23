import requests
import json
from .status_response import *

class SetParamsQuery():
    def __init__(self, params, user_key):
        self.params = params
        self.user_key = user_key

    def run(self):
        payload = {'params': self.params.__dict__,\
            'user_key': self.user_key.__dict__}
        r = requests.post('http://api.routable.ai/dispatcher/params', data = json.dumps(payload))
        return StatusResponse(status = r.json().get('status'),\
            error = r.json().get('error'))
from all_api_calls import *
from structures import *

class RequestQuery():
    def __init__(self, api_key):
        self.api_key = api_key

    def set_fleet_key(self, fleet_key):
        self.fleet_key = fleet_key

    def create_simulated_fleet(self, params):
        payload = {'api_key': self.api_key,\
            'params': params.__dict__}
        r = requests.post('http://api.routable.ai/dispatcher/simulation/create', data = json.dumps(payload))
        return r.json()

    def compute_assignments(self, current_time = None):
        params = {'api_key': self.api_key,\
            'fleet_key': self.fleet_key}
        if current_time:
            params['current_time'] = current_time.isoformat()
        r = requests.get('http://api.routable.ai/dispatcher/assignments', params = params)
        return r.json()
    
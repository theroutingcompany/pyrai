import datetime
import requests

class ComputeAssignmentsQuery():
    def __init__(self, api_key, fleet_key, current_time = None):
        self.api_key = api_key
        self.fleet_key = fleet_key
        self.current_time = current_time

    def run(self):
        params = {'api_key': self.api_key,\
            'fleet_key': self.fleet_key}
        if self.current_time:
            params['current_time'] = self.current_time.isoformat()
        r = requests.get('http://api.routable.ai/dispatcher/assignments', params = params)
        return r.json()
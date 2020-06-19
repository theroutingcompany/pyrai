import datetime
import requests

def compute_assignments(api_key, fleet_key, current_time):
    params = {'api_key': api_key,\
        'fleet_key': fleet_key,\
        'current_time': current_time.isoformat()}
    r = requests.get('http://api.routable.ai/dispatcher/assignments', params = params)
    return r
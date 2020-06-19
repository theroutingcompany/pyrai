import requests
import fleet_params

def create_simulated_fleet(api_key, params):
    payload = {'api_key': api_key,\
        'params': params.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/live/create', data = payload)
    return r
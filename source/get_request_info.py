import requests

def get_request_info(api_key, fleet_key, id):
    params = {'api_key': api_key,\
        'fleet_key': fleet_key,\
        'id': id}
    r = requests.get('http://api.routable.ai/dispatcher/request', params = params)
    return r

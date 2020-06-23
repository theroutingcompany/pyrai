import requests

def get_vehicle_info(api_key, fleet_key, id):
    params = {'api_key': api_key,\
        'fleet_key': fleet_key,\
        'id': id}
    r = requests.get('http://api.routable.ai/dispatcher/vehicle', params = params)
    return r

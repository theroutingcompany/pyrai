import requests
import location
import user_key

def get_vehicle_info(location, id, user_key):
    payload = {'location': location.__dict__,\
        'id': id,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/vehicle/offline',\
        data = payload)
    return r
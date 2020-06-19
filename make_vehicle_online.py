import requests
import location
import user_key

def get_vehicle_info(location, id, capacity, user_key):
    payload = {'location': location.__dict__,\
        'id': id,\
        'capacity': capacity,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/vehicle/online',\
        data = payload)
    return r
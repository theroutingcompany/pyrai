import requests
import fleet_params
import user_key

def set_params(params, user_key):
    payload = {'params': params.__dict__,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/params', data = payload)
    return r
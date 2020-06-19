import requests
import datetime
import location

def add_request(id, pickup, dropoff, load, request_time, user_key):
    payload = {'id': id,\
        'pickup': pickup.__dict__,\
        'dropoff': dropoff.__dict__,\
        'load': load,\
        'request_time': request_time.isoformat(),\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/request/add', data = payload)
    return r
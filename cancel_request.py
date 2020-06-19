import requests
import datetime
import location

def cancel_request(id, event_time, user_key):
    payload = {'id': id,\
        'event_time': event_time.isoformat(),\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/request/cancel', data = payload)
    return r
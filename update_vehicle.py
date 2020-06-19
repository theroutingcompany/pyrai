import requests
import location
import user_key
import event
import datetime

def update_vehicle(id, location, direction, event_time, req_id, event, user_key):
    payload = {'id': id,\
        'location': location.__dict__,\
        'direction': direction,\
        'event_time': event_time.isoformat(),\
        'req_id': req_id,\
        'event': event,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/vehicle/update',\
        data = payload)
    return r
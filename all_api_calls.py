import requests
import datetime
import location
import event
import fleet_params
import user_key

def add_request(id, pickup, dropoff, load, request_time, user_key):
    payload = {'id': id,\
        'pickup': pickup.__dict__,\
        'dropoff': dropoff.__dict__,\
        'load': load,\
        'request_time': request_time.isoformat(),\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/request/add', data = payload)
    return r

def cancel_request(id, event_time, user_key):
    payload = {'id': id,\
        'event_time': event_time.isoformat(),\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/request/cancel', data = payload)
    return r

def compute_assignments(api_key, fleet_key, current_time):
    params = {'api_key': api_key,\
        'fleet_key': fleet_key,\
        'current_time': current_time.isoformat()}
    r = requests.get('http://api.routable.ai/dispatcher/assignments', params = params)
    return r

def create_live_fleet(api_key, params):
    payload = {'api_key': api_key,\
        'params': params.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/live/create', data = payload)
    return r

def create_simulated_fleet(api_key, params):
    payload = {'api_key': api_key,\
        'params': params.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/simulation/create', data = payload)
    return r

def get_request_info(api_key, fleet_key, id):
    params = {'api_key': api_key,\
        'fleet_key': fleet_key,\
        'id': id}
    r = requests.get('http://api.routable.ai/dispatcher/request', params = params)
    return r

def get_vehicle_info(api_key, fleet_key, id):
    params = {'api_key': api_key,\
        'fleet_key': fleet_key,\
        'id': id}
    r = requests.get('http://api.routable.ai/dispatcher/vehicle', params = params)
    return r

def make_vehicle_offline(location, id, user_key):
    payload = {'location': location.__dict__,\
        'id': id,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/vehicle/offline',\
        data = payload)
    return r

def make_vehicle_online(location, id, capacity, user_key):
    payload = {'location': location.__dict__,\
        'id': id,\
        'capacity': capacity,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/vehicle/online',\
        data = payload)
    return r

def query_historical_data(fleet_key, start, end):
    params = {'fleet_key': fleet_key,\
        'start': start.isoformat(),\
        'end': end.isoformat()}
    r = requests.get('http://api.routable.ai/query/vehicles/historical', params = params)
    return r

def remove_vehicle(location, id, user_key):
    payload = {'location': location.__dict__,\
        'id': id,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/vehicle/remove',\
        data = payload)
    return r

def set_params(params, user_key):
    payload = {'params': params.__dict__,\
        'user_key': user_key.__dict__}
    r = requests.post('http://api.routable.ai/dispatcher/params', data = payload)
    return r

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

def visualize_requests(api_key, start, end):
    params = {'api_key': api_key,\
        'start': start.isoformat(),\
        'end': end.isoformat()}
    r = requests.get('https://routable.ai/vis/requests', params = params)
    return r

def visualize_state(api_key, start, end):
    params = {'api_key': api_key,\
        'start': start.isoformat(),\
        'end': end.isoformat()}
    r = requests.get('https://routable.ai/vis/state', params = params)
    return r




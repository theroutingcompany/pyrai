import datetime
import requests

def visualize_state(api_key, start, end):
    params = {'api_key': api_key,\
        'start': start.isoformat(),\
        'end': end.isoformat()}
    r = requests.get('https://routable.ai/vis/state', params = params)
    return r
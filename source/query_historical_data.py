import requests
import datetime

def query_historical_data(fleet_key, start, end):
    params = {'fleet_key': fleet_key,\
        'start': start.isoformat(),\
        'end': end.isoformat()}
    r = requests.get('http://api.routable.ai/query/vehicles/historical', params = params)
    return r
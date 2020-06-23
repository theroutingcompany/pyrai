import requests
import datetime
import json
from .structures import *
from .status_response import *
from dateutil.parser import *

class UpdateVehicleQuery():
    def __init__(self, id, location, direction, event_time, req_id, event, user_key):
        self.id = id
        self.location = location
        self. direction = direction
        self.event_time = event_time
        self.req_id = req_id
        self.event = event
        self.user_key = user_key

    def run(self):
        payload = {'id': self.id,\
            'location': self.location.__dict__,\
            'direction': self.direction,\
            'event_time': self.event_time.astimezone(datetime.timezone.utc).isoformat(),\
            'req_id': self.req_id,\
            'event': self.event,\
            'user_key': self.user_key.__dict__}
        r = requests.post('http://api.routable.ai/dispatcher/vehicle/update',\
            data = json.dumps(payload))
        if r.status_code == 200:
            return UpdateVehicleResponse(r.json().get('veh_id'),\
                Location(r.json().get('location').get('lat'),\
                    r.json().get('location').get('lng')),\
                r.json().get('assigned'),\
                r.json().get('req_ids'),\
                [Event(e.get('req_id'),\
                    Location(e.get('location').get('lat'),\
                        e.get('location').get('lng')),\
                    isoparse(e.get('time')),\
                    e.get('event')\
                    ) for e in r.json().get('events')])
        else:
            return StatusResponse(status = r.json().get('status'),\
                error = r.json().get('error'))

class UpdateVehicleResponse():
    def __init__(self, veh_id, location, assigned, req_ids, events):
        self.veh_id = veh_id
        self.location = location
        self.assigned = assigned
        self.req_ids = req_ids
        self.events = events
    
    def __str__(self):
        return str(self.__dict__)
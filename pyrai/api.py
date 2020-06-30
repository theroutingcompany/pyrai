import urllib.parse
import requests
import datetime
import json
import IPython
from dateutil.parser import *


class FleetParams(object):
    def __init__(self, max_wait, max_delay, unlocked_window, close_pickup_window):
        self.max_wait = max_wait
        self.max_delay = max_delay
        self.unlocked_window = unlocked_window
        self.close_pickup_window = close_pickup_window

    def todict(self):
        return {
            'max_wait': self.max_wait,
            'max_delay': self.max_delay,
            'unlocked_window': self.unlocked_window,
            'close_pickup_window': self.close_pickup_window
        }

class Defaults:
    BASE_URL = "https://api.routable.ai"
    VISUALIZATION_URL = "https://dev.routable.ai/simulation/map?name={}&start={}&end={}&api_key={}&fleet_key={}"
    DEFAULT_CAPACITY = 6
    DEFAULT_DIRECTION = 0
    DEFAULT_PARAMS = FleetParams(
            max_wait="3m",
            max_delay="6m",
            unlocked_window="2m",
            close_pickup_window="1s"
        )


class Endpoints:
    CREATE_SIM_FLEET = "/dispatcher/simulation/create"
    CREATE_LIVE_FLEET = "/dispatcher/live/create"
    MAKE_VEHICLE_ONLINE = "/dispatcher/vehicle/online"
    MAKE_VEHICLE_OFFLINE = "/dispatcher/vehicle/offline"
    UPDATE_VEHICLE = "/dispatcher/vehicle/update"
    REMOVE_VEHICLE = "/dispatcher/vehicle/remove"
    GET_VEHICLE_INFO = "/dispatcher/vehicle"
    ADD_REQUEST = "/dispatcher/request/add"
    GET_REQUEST = "/dispatcher/request"
    CANCEL_REQUEST = "/dispatcher/request/cancel"
    COMPUTE_ASSIGNMENTS = "/dispatcher/assignments"
    SET_PARAMS = "/dispatcher/params"


class Pyrai(object):
    """
    Pyrai docs go here
    """

    def __init__(self, url=Defaults.BASE_URL, api_key=None):
        """
        Docs go here
        """
        self.api_key = api_key
        self.base_url = url
    
    def build_url(self, endpoint):
        return urllib.parse.urljoin(self.base_url, endpoint)

    def todict(self):
        return {
            'api_key': self.api_key,
            'base_url': self.base_url
        }

    def __str__(self):
        return str(self.todict())

    def __create_fleet(
        self, endpoint,
        max_wait="3m", max_delay="6m",
        unlocked_window="2m", close_pickup_window="1s"
    ):
        url = self.build_url(endpoint)
        params = FleetParams(
            max_wait=max_wait,
            max_delay=max_delay,
            unlocked_window=unlocked_window,
            close_pickup_window=close_pickup_window
        )

        payload = {"api_key": self.api_key, "params": params.todict()}
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return Fleet(pyrai=self, fleet_key=resp.get('fleet_key'), params=params)
        else:
            return StatusResponse(resp=resp)

    def create_sim_fleet(
        self, max_wait="3m", max_delay="6m",
        unlocked_window="2m", close_pickup_window="1s"
    ):
        return self.__create_fleet(
            Endpoints.CREATE_SIM_FLEET,
            max_wait=max_wait,
            max_delay=max_delay,
            unlocked_window=unlocked_window,
            close_pickup_window=close_pickup_window,
        )
    
    def create_live_fleet(
        self, max_wait="3m", max_delay="6m",
        unlocked_window="2m", close_pickup_window="1s"
    ):
        return self.__create_fleet(
            Endpoints.CREATE_LIVE_FLEET,
            max_wait=max_wait,
            max_delay=max_delay,
            unlocked_window=unlocked_window,
            close_pickup_window=close_pickup_window,
        )
    

class Fleet(object):
    def __init__(self, fleet_key, params=Defaults.DEFAULT_PARAMS, api_key=None, pyrai=None, vis_url=Defaults.VISUALIZATION_URL):

        if api_key is None:
            api_key = pyrai.api_key

        if pyrai is None:
            pyrai = Pyrai(api_key=api_key)

        self.api_key = api_key
        self.fleet_key = fleet_key
        self.pyrai = pyrai
        self.params = params
        self.vis_url = vis_url
    
    @property
    def user_key(self):
        return UserKey(self.api_key, self.fleet_key)

    def todict(self):
        return {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
        }

    def __str__(self):
        return str(self.todict())

    def build_url(self, endpoint):
        return self.pyrai.build_url(endpoint)

    def set_params(self,
        max_wait=None,
        max_delay=None,
        unlocked_window=None,
        close_pickup_window=None):
        '''
        note that this mutates the fleet object
        '''

        if max_wait is not None:
            self.params.max_wait = max_wait

        if max_delay is not None:
            self.params.max_delay = max_delay

        if unlocked_window is not None:
            self.params.unlocked_window = unlocked_window

        if close_pickup_window is not None:
            self.params.close_pickup_window = close_pickup_window

        url = self.build_url(Endpoints.SET_PARAMS)
        payload = {
            "params": self.params.todict(),
            "user_key": self.user_key.todict()
        }
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp=resp)
    
    def make_vehicle_online(self, vid, location, capacity):
        url = self.build_url(Endpoints.MAKE_VEHICLE_ONLINE)
        payload = {
            "location": location.todict(),
            "id": vid,
            'capacity': capacity,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp=resp)
        
    def make_vehicle_offline(self, vid, location):
        url = self.build_url(Endpoints.MAKE_VEHICLE_OFFLINE)
        payload = {
            'location': location.todict(),
            'id': vid,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp = resp)
    
    def update_vehicle(self, vid, location, direction, event, event_time=datetime.datetime.now(), req_id=None):
        url = self.build_url(Endpoints.UPDATE_VEHICLE)
        payload = {
            'id': vid,
            'location': location.todict(),
            'direction': direction,
            'event_time': to_rfc3339(event_time),
            'event': event,
            'user_key': self.user_key.todict()
        }
        
        if req_id is not None:
            payload['req_id'] = req_id
        
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return Vehicle.fromdict(self, resp)
        else:
            return StatusResponse(resp = resp)

    def remove_vehicle(self, vid, location):
        url = self.build_url(Endpoints.REMOVE_VEHICLE)
        payload = {
            'location': location.todict(),
            'id': vid,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return resp.get('req_ids')
        else:
            return StatusResponse(resp = resp)
            
    # need to update to use GraphQL but the endpoint doesn't work as expected?
    def get_vehicle_info(self, vid):
        url = self.build_url(Endpoints.GET_VEHICLE_INFO)
        params = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
            'id': vid
        }
        r = requests.get(url, params = params)
        resp = r.json()

        if r.status_code == 200:
            return Vehicle.fromdict(self, resp)
        else:
            return StatusResponse(resp=resp) 
    
    def add_request(self, rid, pickup, dropoff, load, request_time):
        url = self.build_url(Endpoints.ADD_REQUEST)
        payload = {
            'id': rid,
            'pickup': pickup.todict(),
            'dropoff': dropoff.todict(),
            'load': load,
            'request_time': to_rfc3339(request_time),
            'user_key': self.user_key.todict()
        }

        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp = resp)

    def cancel_request(self, rid, event_time):
        url = self.build_url(Endpoints.CANCEL_REQUEST)
        payload = {
            'id': rid,
            'event_time': to_rfc3339(event_time),
            'user_key': self.user_key.todict()
        }

        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp = resp)

    def get_request(self, rid):
        url = self.build_url(Endpoints.GET_REQUEST)
        payload = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
            'id': rid
        }

        r = requests.get(url, params=payload)
        resp = r.json()
        
        if r.status_code == 200:
            return Request.fromdict(self, resp)
        else:
            return StatusResponse(resp=resp) 


    def get_assignments(self, current_time=None):
        url = self.build_url(Endpoints.COMPUTE_ASSIGNMENTS)
        payload = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key
        }

        if current_time is not None:
            payload['current_time'] = to_rfc3339(current_time)

        r = requests.get(url, params=payload)
        resp = r.json()

        if r.status_code == 200:
            return VehicleAssignments(
                vehs=[Vehicle.fromdict(self, veh) for veh in resp.get('vehs')],
                requests=[Request.fromdict(self, req) for req in resp.get('reqs')],
                notifications=[Notification.fromdict(notif) for notif in resp.get('notifications')],
            )
        else:
            return StatusResponse(resp = resp)

    def visualize_state(self, start_time, end_time):
        url = self.vis_url.format("state", 
            to_rfc3339(start_time), 
            to_rfc3339(end_time), 
            self.api_key, 
            self.fleet_key)
        return IPython.display.IFrame(url, 800, 500)

    def visualize_requests(self, start_time, end_time):
        url = self.vis_url.format("requests", 
            to_rfc3339(start_time), 
            to_rfc3339(end_time), 
            self.api_key, 
            self.fleet_key)
        return IPython.display.IFrame(url, 800, 500)


def to_rfc3339(dt):
    return dt.astimezone(datetime.timezone.utc).isoformat()[:-6] + "Z"


class Vehicle():
    def __init__(self, fleet, veh_id, location, assigned, req_ids, events):
        self.fleet = fleet
        self.veh_id = veh_id
        self.location = location
        self.assigned = assigned
        self.req_ids = req_ids
        self.events = events
    
    @staticmethod
    def fromdict(fleet, d):
        return Vehicle(
            fleet,
            d.get('veh_id'),
            Location.fromdict(d.get('location')),
            d.get('assigned'),
            d.get('req_ids'),
            [Event.fromdict(e) for e in d.get('events')]
        )

    def todict(self):
        return {
            'fleet': self.fleet.todict(),
            'veh_id': self.veh_id,
            'location': self.location.todict(),
            'assigned': self.assigned,
            'req_ids': self.req_ids,
            'events': [e.todict() for e in self.events]
        }

    def __str__(self):
        return str(self.todict())

    def make_online(self, location=None, capacity=Defaults.DEFAULT_CAPACITY):

        if location is None:
            location = self.location

        return self.fleet.make_vehicle_online(self.veh_id, location, capacity)

    def make_offline(self, location=None):

        if location is None:
            location = self.location

        return self.fleet.make_vehicle_offline(self.veh_id, location)

    def update(self, 
        event,
        req_id=None,
        location=None, 
        direction=Defaults.DEFAULT_DIRECTION, 
        event_time=None):
        '''
        note that this mutates the input veh
        '''
        
        if location is None:
            location = self.location
        
        if event_time is None:
            event_time = datetime.datetime.now()

        updated_veh = self.fleet.update_vehicle(
            vid=self.veh_id,
            location=location,
            direction=direction,
            event_time=event_time,
            req_id=req_id,
            event=event
        )

        self.location = updated_veh.location
        self.assigned = updated_veh.assigned
        self.req_ids = updated_veh.req_ids
        self.events = updated_veh.events

        return

    def remove(self, location=None):
        
        if location is None:
            location = self.location

        return self.fleet.remove_vehicle(self.veh_id, location)


class UserKey(object):
    def __init__(self, api_key, fleet_key):
        self.api_key = api_key
        self.fleet_key = fleet_key
    
    def todict(self):
        return {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key
        }

    def __str__(self):
        return str(self.todict())


class Location(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    
    @staticmethod
    def fromdict(d):
        return Location(d.get('lat'), d.get('lng'))

    def todict(self):
        return {
            'lat': self.lat,
            'lng': self.lng
        }

    def __str__(self):
        return str(self.todict())


class Request():
    def __init__(self, fleet, pickup, dropoff, request_time, req_id, veh_id, load, assigned):
        self.fleet = fleet
        self.pickup = pickup
        self.dropoff = dropoff
        self.request_time = request_time
        self.req_id = req_id
        self.veh_id = veh_id
        self.load = load
        self.assigned = assigned

    @staticmethod
    def fromdict(fleet, d):
        return Request(
            fleet,
            Location.fromdict(d.get('pickup')),
            Location.fromdict(d.get('dropoff')),
            isoparse(d.get('request_time')),
            d.get('req_id'),
            d.get('veh_id'),
            d.get('load'),
            d.get('assigned')
        )
    
    def todict(self):
        return {
            'fleet': self.fleet.todict(),
            'pickup': self.pickup.todict(),
            'dropoff': self.dropoff.todict(),
            'request_time': to_rfc3339(self.request_time),
            'req_id': self.req_id,
            'veh_id': self.veh_id,
            'load': self.load,
            'assigned': self.assigned
        }

    def __str__(self):
        return str(self.todict())

class Event(object):
    def __init__(self, req_id, location, time, event):
        self.req_id = req_id
        self.location = location
        self.time = time
        self.event = event

    @staticmethod
    def fromdict(d):
        return Event(
            d.get('req_id'),
            Location.fromdict(d.get('location')),
            isoparse(d.get('time')),
            d.get('event')
        )

    def todict(self):
        return {
            'req_id': self.req_id,
            'location': self.location.todict(),
            'time': to_rfc3339(self.time),
            'event': self.event
        }
    
    def __str__(self):
        return str(self.todict())

class Notification():
    def __init__(self, message, data):
        self.message = message
        self.data = data
    
    @staticmethod
    def fromdict(d):
        return Notification(
            d.get('message'),
            NotificationData.fromdict(d.get('data'))
        )

    def todict(self):
        return {
            'message': self.message,
            'data': self.data.todict()
        }

    def __str__(self):
        return str(self.todict())

class NotificationData():
    def __init__(self, veh_id, req_id, waiting_duration, assigned):
        self.veh_id = veh_id
        self.req_id = req_id
        self.waiting_duration = waiting_duration
        self.assigned = assigned

    @staticmethod
    def fromdict(d):
        return NotificationData(
            d.get('veh_id'),
            d.get('req_id'),
            d.get('waiting_duration'),
            d.get('assigned')
        )

    def todict(self):
        return {
            'veh_id': self.veh_id,
            'req_id': self.req_id,
            'waiting_duration': self.waiting_duration,
            'assigned': self.assigned
        }

    def __str__(self):
        return str(self.todict())

class StatusResponse(object):
    def __init__(self, resp=None, status=None, error=None):
        if resp is not None:
            self.status = resp.get('status')
            self.error = resp.get('error')
        else:
            self.status = status
            self.error = error

    def todict(self):
        return {
            'status': self.status,
            'error': self.error
        }

    def __str__(self):
        return str(self.todict())


class VehicleAssignments(object):
    def __init__(self, vehs=[], requests=[], notifications=[]):
        self.vehs = vehs
        self.requests = requests
        self.notifications = notifications

    def todict(self):
        return {
            'vehs': [v.todict() for v in self.vehs], 
            'requests': [r.todict() for r in self.requests],
            'notifications': [n.todict() for n in self.notifications]
        }

    def __str__(self):
        return str(self.todict())


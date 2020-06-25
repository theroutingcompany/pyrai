import urllib.parse
import requests
import datetime
import json
from dateutil.parser import *

class Defaults:
    BASE_URL = "http://api.routable.ai"
    DEFAULT_CAPACITY = 6
    DEFAULT_DIRECTION = 0


class Endpoints:
    CREATE_SIM_FLEET = "/dispatcher/simulation/create"
    CREATE_LIVE_FLEET = "/dispatcher/live/create"
    MAKE_VEHICLE_ONLINE = "/dispatcher/vehicle/online"
    MAKE_VEHICLE_OFFLINE = "/dispatcher/vehicle/offline"
    UPDATE_VEHICLE = "/dispatcher/vehicle/update"
    REMOVE_VEHICLE = "/dispatcher/vehicle/remove"
    GET_VEHICLE_INFO = "/dispatcher/vehicle"
    ADD_REQUEST = "/dispatcher/request/add"
    CANCEL_REQUEST = "/dispatcher/request/cancel"
    COMPUTE_ASSIGNMENTS = "/dispatcher/assignments"


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
            return Fleet(pyrai=self, fleet_key=resp.get('fleet_key'))
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
    def __init__(self, pyrai, fleet_key):
        self.api_key = pyrai.api_key
        self.fleet_key = fleet_key
        self.pyrai = pyrai
    
    @property
    def user_key(self):
        return UserKey(self.api_key, self.fleet_key)

    def build_url(self, endpoint):
        return self.pyrai.build_url(endpoint)
    
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
    
    def update_vehicle(self, vid, location, direction, event_time, req_id, event):
        url = self.build_url(Endpoints.UPDATE_VEHICLE)
        payload = {
            'id': vid,
            'location': location.todict(),
            'direction': direction,
            'event_time': to_rfc3339(event_time),
            'req_id': req_id,
            'event': event,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return Vehicle.fromdict(self.user_key, resp)
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
            return Vehicle.fromdict(self.user_key, resp)
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

        r = requests.post(url, data = payload)
        resp = r.json()
        return StatusResponse(resp = resp)


    def compute_assignments(self, current_time):
        url = self.build_url(Endpoints.COMPUTE_ASSIGNMENTS)
        payload = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
            'current_time': to_rfc3339(current_time)
        }

        r = requests.post(url, data = payload)
        resp = r.json()

        if r.status_code == 200:
            return VehicleAssignments(
                vehs=[Vehicle.fromdict(self.user_key, veh) for veh in resp.get('vehs')],
                requests=[Request.fromdict(self.user_key, req) for req in resp.get('reqs')],
                notifications=[Notification.fromdict(notif) for notif in resp.get('notifications')],
            )
        else:
            return StatusResponse(resp = resp)


def to_rfc3339(dt):
    return dt.astimezone(datetime.timezone.utc).isoformat()


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

    def make_online(self, location=None, capacity=Defaults.DEFAULT_CAPACITY):

        if location is None:
            location = self.location

        return self.fleet.make_vehicle_online(self.veh_id, location, capacity)

    def make_offline(self, location=None):

        if location is None:
            location = self.location

        return self.fleet.make_vehicle_offline(self.veh_id, location)

    def update(self, 
        req_id,
        event,
        location=None, 
        direction=Defaults.DEFAULT_DIRECTION, 
        event_time=None):
        
        if location is None:
            location = self.location
        
        if event_time is None:
            event_time = datetime.datetime.now()

        return self.fleet.update_vehicle(
            self.veh_id,
            location,
            direction,
            event_time,
            req_id,
            event
        )

    def remove(self, location=None):
        
        if location is None:
            location = self.location

        return self.fleet.remove_vehicle(self.veh_id, location)

    def __str__(self):
        return str(self.__dict__)


class UserKey(object):
    def __init__(self, api_key, fleet_key):
        self.api_key = api_key
        self.fleet_key = fleet_key
    
    def todict(self):
        return {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key
        }


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
        return str(self.__dict__)


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
            'request_time': isoparse(self.request_time),
            'req_id': self.req_id,
            'veh_id': self.veh_id,
            'load': self.load,
            'assigned': self.assigned
        }

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
            'time': isoparse(self.time),
            'event': self.event
        }

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

class StatusResponse(object):
    def __init__(self, resp=None, status=None, error=None):
        if resp is not None:
            self.status = resp.get('status')
            self.error = resp.get('error')
        else:
            self.status = status
            self.error = error

    def __str__(self):
        return str(self.__dict__)


class VehicleAssignments(object):
    def __init__(self, vehs=[], requests=[], notifications=[]):
        self.vehs = vehs
        self.requests = requests
        self.notifications = notifications

rai = Pyrai(api_key="abcd-efgh")
sim = rai.create_sim_fleet(max_wait="3m", max_delay="6m",)
veh = sim.make_vehicle_online(id=1, location=Location(12.1, 31.3), capacity=10)
sim.make_vehicle_offline(veh)

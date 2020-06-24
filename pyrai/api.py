import urlparse
import requests
import datetime
import json
from dateutil.parser import *

class Defaults:
    BASE_URL = "http://api.routable.ai"


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
        return build_url(self.base_url, endpoint)

    def __create_fleet(
        self, endpoint,
        max_wait="3m", max_delay="6m",
        unlocked_window="2m", close_pickup_window="1s"
    ):
        url = self.build_url(endpoint = endpoint)
        params = FleetParams(
            max_wait=max_wait,
            max_delay=max_delay,
            unlocked_window=unlocked_window,
            close_pickup_window=close_pickup_window
        )

        payload = {"api_key": self.api_key, "params": dict(params)}
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return Fleet(api_key=self.api_key, fleet_key=resp.get('fleet_key'))
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
    def __init__(self, api_key, fleet_key, base_url=Defaults.BASE_URL):
        self.api_key = api_key
        self.fleet_key = fleet_key
        self.base_url = base_url
    
    @property
    def user_key(self):
        return UserKey(self.api_key, self.fleet_key)

    def build_url(self, endpoint):
        return build_url(self.base_url, endpoint)
    
    def make_vehicle_online(self, vid, location, capacity):
        url = self.build_url(Endpoints.MAKE_VEHICLE_ONLINE)
        payload = {
            "location": dict(location),
            "id": vid,
            'capacity': capacity,
            'user_key': dict(self.user_key)
        }
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp=resp)
        
    def make_vehicle_offline(self, vid, location):
        url = self.build_url(Endpoints.MAKE_VEHICLE_OFFLINE)
        payload = {
            'location': dict(location),
            'id': vid,
            'user_key': dict(self.user_key)
        }
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp = resp)
    
    def update_vehicle(self, vid, location, direction, event_time, req_id, event, users):
        url = self.build_url(Endpoints.UPDATE_VEHICLE)
        payload = {
            'id': vid,
            'location': dict(location),
            'direction': direction,
            'event_time': to_rfc3339(event_time),
            'req_id': req_id,
            'event': event,
            'user_key': dict(self.user_key)
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
            'location': dict(location),
            'id': vid,
            'user_key': dict(self.user_key)
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
            'pickup': dict(pickup),
            'dropoff': dict(dropoff),
            'load': load,
            'request_time': to_rfc3339(request_time),
            'user_key': dict(self.user_key)
        }

        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()
        return StatusResponse(resp = resp)

    def cancel_request(self, rid, event_time):
        url = self.build_url(Endpoints.CANCEL_REQUEST)
        payload = {
            'id': rid,
            'event_time': to_rfc3339(event_time),
            'user_key': dict(self.user_key)
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

def build_url(base_url, endpoint):
    return urlparse.urljoin(base_url, endpoint)

class Vehicle():
    def __init__(self, user_key, veh_id, location, assigned, req_ids, events):
        self.user_key = user_key
        self.veh_id = veh_id
        self.location = location
        self.assigned = assigned
        self.req_ids = req_ids
        self.events = events
    
    @staticmethod
    def fromdict(user_key, d):
        return Vehicle(
            user_key,
            d.get('veh_id'),
            Location.fromdict(d.get('location')),
            d.get('assigned'),
            d.get('req_ids'),
            d.get('events')
        )

    def make_vehicle_online(self):
        pass

    def make_vehicle_offline(self):
        pass    

    def update_vehicle(self):
        pass

    def remove_vehicle(self):
        pass

    def __str__(self):
        return str(self.__dict__)


class UserKey(object):
    def __init__(self, api_key, fleet_key):
        self.api_key = api_key
        self.fleet_key = fleet_key


class Location(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    
    @staticmethod
    def fromdict(d):
        return Location(d.get('lat'), d.get('lng'))

    def __str__(self):
        return str(self.__dict__)


class Request():
    def __init__(self, user_key, pickup, dropoff, request_time, req_id, veh_id, load, assigned):
        self.user_key = user_key
        self.pickup = pickup
        self.dropoff = dropoff
        self.request_time = request_time
        self.req_id = req_id
        self.veh_id = veh_id
        self.load = load
        self.assigned = assigned

    @staticmethod
    def fromdict(user_key, d):
        return Request(
            user_key,
            Location.fromdict(d.get('pickup')),
            Location.fromdict(d.get('dropoff')),
            isoparse(d.get('request_time')),
            d.get('req_id'),
            d.get('veh_id'),
            d.get('load'),
            d.get('assigned')
        )

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

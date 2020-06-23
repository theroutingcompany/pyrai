from dateutil.parser import *

class Event():
    def __init__(self, req_id, location, time, event):
        self.req_id = req_id
        self.location = location
        self.time = time
        self.event = event

    @staticmethod
    def fromdict(d):
        return Event(d.get('req_id'),\
            Location.fromdict(d.get('location')),\
            isoparse(d.get('time')),\
            d.get('event'))

class UserKey:
    def __init__(self, api_key, fleet_key):
        self.api_key = api_key
        self.fleet_key = fleet_key

class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    
    @staticmethod
    def fromdict(d):
        return Location(d.get('lat'), d.get('lng'))

    def __str__(self):
        return str(self.__dict__)

class FleetParams():
    def __init__(self, max_wait, max_delay, unlocked_window, close_pickup_window):
        self.max_wait = max_wait
        self.max_delay = max_delay
        self.unlocked_window = unlocked_window
        self.close_pickup_window = close_pickup_window

class Vehicle():
    def __init__(self, veh_id, location, assigned, req_ids, events):
        self.veh_id = veh_id
        self.location = location
        self.assigned = assigned
        self.req_ids = req_ids
        self.events = events
    
    @staticmethod
    def fromdict(d):
        return Vehicle(\
            d.get('veh_id'),\
            Location.fromdict(d.get('location')),\
            d.get('assigned'),\
            d.get('req_ids'),\
            d.get('events'))

    def __str__(self):
        return str(self.__dict__)

class Request():
    def __init__(self, pickup, dropoff, request_time, req_id, veh_id, load, assigned):
        self.pickup = pickup
        self.dropoff = dropoff
        self.request_time = request_time
        self.req_id = req_id
        self.veh_id = veh_id
        self.load = load
        self.assigned = assigned

    @staticmethod
    def fromdict(d):
        return Request(\
            Location.fromdict(d.get('pickup')),\
            Location.fromdict(d.get('dropoff')),\
            isoparse(d.get('request_time')),\
            d.get('req_id'),\
            d.get('veh_id'),\
            d.get('load'),\
            d.get('assigned'))

class Notification():
    class NotificationData():
        def __init__(self, veh_id, req_id, waiting_duration, assigned):
            self.veh_id = veh_id
            self.req_id = req_id
            self.waiting_duration = waiting_duration
            self.assigned = assigned

        @staticmethod
        def fromdict(d):
            return NotificationData(\
                d.get('veh_id'),\
                d.get('req_id'),\
                d.get('waiting_duration'),\
                d.get('assigned'))

    def __init__(self, message, data):
        self.message = message
        self.data = data
    
    @staticmethod
    def fromdict(d):
        return Notification(\
            d.get('message'),\
            NotificationData.fromdict(d.get('data'))\
        )
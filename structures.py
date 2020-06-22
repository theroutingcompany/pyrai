from enum import Enum

class Event(Enum):
    PICKUP = 'pickup'
    DROPOFF = 'dropoff'
    PROGRESS = 'progress'
    UNASSIGNED = 'unassigned'

class UserKey:
    def __init__(self, api_key, fleet_key):
        self.api_key = api_key
        self.fleet_key = fleet_key

class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    
class FleetParams():
    def __init__(self, max_wait, max_delay, unlocked_window, close_pickup_window):
        self.max_wait = max_wait
        self.max_delay = max_delay
        self.unlocked_window = unlocked_window
        self.close_pickup_window = close_pickup_window

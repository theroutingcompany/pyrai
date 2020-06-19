from enum import Enum

class Event(Enum):
    PICKUP = 'pickup'
    DROPOFF = 'dropoff'
    PROGRESS = 'progress'
    UNASSIGNED = 'unassigned'
from .location import Location
from dateutil.parser import isoparse
from pyrai.helpers import to_rfc3339

class Event(object):
    """
    Class used for representing events.

    Attributes:
        req_id (int): the ID of the request corresponding to this event
        location (Location): the event Location
        time (datetime.datetime): the event time.
        event (VehicleEvent): the vehicle event corresponding to the event.
    """
    def __init__(self, req_id, location, time, event):
        """
        Initializes an Event object.

        Args:
            req_id (int): the ID of the request corresponding to this event
            location (Location): the event Location
            time (datetime.datetime): the event time.
            event (VehicleEvent): the vehicle event corresponding to the event.
        """
        self.req_id = req_id
        self.location = location
        self.time = time
        self.event = event

    @staticmethod
    def fromdict(d):
        """
        Converts a python dictionary to an Event object.

        Args:
            d (dict): The dictionary to convert.

        Returns:
            Event: An event with the parameters set by the values in d.
        """
        return Event(
            d.get('req_id'),
            Location.fromdict(d.get('location')),
            isoparse(d.get('time')),
            d.get('event')
        )

    def todict(self):
        """
        Converts an Event to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'req_id': self.req_id,
            'location': self.location.todict(),
            'time': to_rfc3339(self.time),
            'event': self.event
        }
    
    def __str__(self):
        return str(self.todict())
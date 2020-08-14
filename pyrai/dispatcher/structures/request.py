import datetime
from pyrai.helpers import to_rfc3339
from pyrai.dispatcher.structures.location import Location
from dateutil.parser import isoparse

class Request(object):
    """
    Class for representing requests.

    Attributes:
        fleet (Fleet): The fleet that the request is a part of.
        pickup (Location): The pickup location.
        dropoff (Location): The dropoff location.
        request_time (datetime.datetime): The request time.
        req_id (int): The request ID.
        veh_id (int): The ID of the Vehicle corresponding to this request. 
            -1 if unassigned.
        load (int): The load (number of passengers) in this request.
        assigned (boolean): True if assigned, false if not.
    """
    def __init__(self, fleet, pickup, dropoff, request_time, req_id, veh_id, load, assigned):
        """
        Initializes a new Request Object.

        Args:
            fleet (Fleet): The fleet that the request is a part of.
            pickup (Location): The pickup location.
            dropoff (Location): The dropoff location.
            request_time (datetime.datetime): The request time.
            req_id (int): The request ID.
            veh_id (int): The ID of the Vehicle corresponding to this request. 
                -1 if unassigned.
            load (int): The load (number of passengers) in this request.
            assigned (boolean): True if assigned, false if not.
        """

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
        """
        Converts a python dict into a Request object.

        Args:
            fleet (Fleet): The fleet the request is part of.
            d (dict): The dictionary with the request parameters.

        Returns:
            Request: A request initialized with the parameters defined by d.
        """
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
        """
        Converts a Request to a python dict.

        Returns:
            dict: A dictionary representation of self.
        """
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

    def cancel(self, event_time=None):
        """
        Cancels a request.

        Args:
            event_time (datetime.datetime, optional): The event time. 
                Set to datetime.datetime.now() if not provided. Defaults to None.

        Returns:
            Status Response: If successful.

        Raises:
            StatusError: If unsuccessful.
        """
        if event_time is None:
            event_time = datetime.datetime.now()

        return self.fleet.cancel_request(self.req_id, event_time)

    def __str__(self):
        return str(self.todict())

    def __repr__(self):
        return str(self.todict())
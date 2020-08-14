from .location import Location
from .event import Event
from dateutil.parser import isoparse
from .defaults import Defaults

class Vehicle(object):
    """ 
    Class used to represent vehicles.

    Attributes:
        fleet (Fleet): the fleet the vehicle is a part of.
        veh_id (int): the unique ID of the vehicle.
        location (Locaiton): the location of the vehicle.
        assigned (boolean): True if vehicle is assigned, false if not.
        req_ids (list[int]): list of request IDs of assigned requests.
        events (list[Event]): list of events this vehicle is assigned to.

    """
    def __init__(self, fleet, veh_id, location, assigned, req_ids, events):
        """
        Initializes a vehicle object

        Args:
            fleet (Fleet): the fleet the vehicle is a part of.
            veh_id (int): the unique ID of the vehicle.
            location (Locaiton): the location of the vehicle.
            assigned (boolean): True if vehicle is assigned, false if not.
            req_ids (list[int]): list of request IDs of assigned requests.
            events (list[Event]): list of events this vehicle is assigned to.
        """

        self.fleet = fleet
        self.veh_id = veh_id
        self.location = location
        self.assigned = assigned
        self.req_ids = req_ids
        self.events = events
    
    @staticmethod
    def fromdict(fleet, d):
        """
        Converts a python dictionary into a Vehicle object.

        Args:
            fleet (Fleet): The fleet the vehicle is part of.
            d (dict): The dictionary with the vehicle parameters.

        Returns:
            Vehicle: A vehicle object with the parameters the dictionary specifes.
        """

        return Vehicle(
            fleet,
            d.get('veh_id'),
            Location.fromdict(d.get('location')),
            d.get('assigned'),
            d.get('req_ids'),
            [Event.fromdict(e) for e in d.get('events')]
        )

    def todict(self):
        """
        Converts the Vehicle object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """

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

    # eventually want to move the below calls to dispatcher/methods
    def make_online(self, location=None, capacity=Defaults.DEFAULT_CAPACITY):
        """
        Makes vehicle online.

        Args:
            location (Lovation, optional): Location of vehicle, uses self.location
                if nothing is provided. Defaults to None.
            capacity (int, optional): The capacity of the vehicle.
                Defaults to Defaults.DEFAULT_CAPACITY.

        Returns:
            StatusResponse: If successful.
        
        Raises:
            StatusError: If unsuccessful.
        """

        if location is None:
            location = self.location

        return self.fleet.make_vehicle_online(self.veh_id, location, capacity)

    def make_offline(self, location=None):
        """
        Makes vehicle offline.

        Args:
            location (Lovation, optional): Location of vehicle, uses self.location
                if nothing is provided. Defaults to None.

        Returns:
            StatusResponse: If successful.
        
        Raises:
            StatusError: If unsuccessful.
        """

        if location is None:
            location = self.location

        return self.fleet.make_vehicle_offline(self.veh_id, location)

    def update(self, 
        event,
        req_id=None,
        location=None, 
        direction=Defaults.DEFAULT_DIRECTION, 
        event_time=None):
        """
        Updates the vehicle. Note that this mutates the vehicle, so nothing is returned.

        Args:
            location (Location, optional): The vehicle location, set to self.location
                if nothing is provided. Defaults to None.
            direction (float, optional): Angle in radians clockwise away from true north.
                Defaults to Defaults.DEFAULT_DIRECTION.
            event (VehicleEvent): Describes the current event for the vehicle. 
                pickup occurs when the vehicle has picked up a request. 
                dropoff occurs when the vehicle has dropped of a request. 
                progress should be set when the vehicle is moving to service a request, 
                either picking up or dropping off. The vehicle should be marked as 
                unassigned when it is is not assigned to any requests.
            event_time (datetime.datetime, optional): Time at which the vehicle update has occurred. Set to datetime.datetime.now() if not provided. Defaults to None.
            req_id (int, optional): The unique ID of request the vehicle is servicing. 
                If the vehicle is unassigned, this may be omitted. Defaults to None.

        Returns:
            None

        Raises:
            StatusError: If unsuccessful.
        """
        
        if location is None:
            location = self.location

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
        """
        Removes the vehicle.

        Args:
            location (Location, optional): The location of the vehicle,
                will be set to self.location if nothing is provided.
                Defaults to None.

        Returns:
            StatusResponse: If successful.

        Raises:
            StatusError: If unsuccessful.
        """
        
        if location is None:
            location = self.location

        return self.fleet.remove_vehicle(self.veh_id, location)

    def __repr__(self):
        return str(self.todict())

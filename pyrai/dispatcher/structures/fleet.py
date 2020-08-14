from .defaults import Defaults
from .user_key import UserKey
import datetime
from dateutil.parser import isoparse
import requests
import json
from pyrai.helpers import to_rfc3339
from pytimeparse.timeparse import timeparse

class Fleet(object):
    """
    Class used to represent a fleet. All vehicle, request, and
    assignment API calls are methods of this class.

    Attributes:
        pyrai (string): The Pyrai object this fleet was built from.
        fleet_key (string): The fleet key corresponding to this fleet.
        api_key (string): The API key corresponding to this fleet.
        params (FleetParams): The parameters of this fleet.
        vis_url (string): The URL used for visualizations. 
    """

    def __init__(self,
        api_key, 
        fleet_key, 
        params=Defaults.DEFAULT_PARAMS,
        vis_url=Defaults.VISUALIZATION_URL, 
        base_url=Defaults.BASE_URL):
        """
        Initializes a Fleet object.

        Args:
            fleet_key (string): The fleet key.
            params (FleetParams, optional): The fleet parameters. Defaults to Defaults.DEFAULT_PARAMS.
            api_key (string, optional): The API key. Defaults to None.
            pyrai (Pyrai, optional): The Pyrai object this fleet was built from.
                If the fleet is created without a Pyrai object, one is created.
                Defaults to None.
            vis_url (string, optional): The URL used for visualization. Defaults to Defaults.VISUALIZATION_URL.
            base_url (string, optional): The base URL used for API calls. This is
                used when a user wants to create a fleet without creating a fleet from
                a Pyrai object (e.g. using a predetermined fleet key).
                Defaults to Defaults.BASE_URL.
        """

        self.api_key = api_key
        self.fleet_key = fleet_key
        self.base_url = base_url
        self.params = params
        self.vis_url = vis_url
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
    
    @property
    def user_key(self):
        """
        UserKey: UserKey object corresponding to the fleet. 
        """
        return UserKey(self.api_key, self.fleet_key)

    def todict(self):
        """
        Converts the Fleet object into a python dictionary. Note
        that this does not contain all attributes.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
        }

    def __str__(self):
        return str(self.todict())

    from pyrai.helpers import build_url

    from pyrai.dispatcher.methods.fleet.make_vehicle_online import make_vehicle_online
    from pyrai.dispatcher.methods.fleet.make_vehicle_offline import make_vehicle_offline
    from pyrai.dispatcher.methods.fleet.update_vehicle import update_vehicle
    from pyrai.dispatcher.methods.fleet.remove_vehicle import remove_vehicle
    from pyrai.dispatcher.methods.fleet.get_vehicle_info import get_vehicle_info
    from pyrai.dispatcher.methods.fleet.set_params import set_params
    from pyrai.dispatcher.methods.fleet.add_request import add_request
    from pyrai.dispatcher.methods.fleet.cancel_request import cancel_request
    from pyrai.dispatcher.methods.fleet.get_request import get_request
    from pyrai.dispatcher.methods.fleet.get_assignments import get_assignments
    from pyrai.dispatcher.methods.fleet.forward_simulate import forward_simulate
    from pyrai.dispatcher.methods.fleet.plot_metrics import plot_metrics
    from pyrai.dispatcher.methods.fleet.visualize import visualize
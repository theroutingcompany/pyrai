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

    from pyrai.dispatcher.methods.fleet import make_vehicle_online, make_vehicle_offline, update_vehicle, remove_vehicle, get_vehicle_info, set_params, add_request, cancel_request, get_request, get_assignments, forward_simulate, plot_metrics, visualize
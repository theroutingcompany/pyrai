from .defaults import Defaults
from .fleet import Fleet
from .endpoints import Endpoints
from .status_error import StatusError
from .fleet_params import FleetParams
import requests
import json
import urllib.parse


class Pyrai(object):
    """
    Class used to connect to API with API key (no fleet key).

    Attributes:
        api_key (str): The API key. Defaults to None.
        base_url (str): The url of the API service. Defaults to 
            "https://api.routable.ai/"
    """

    def __init__(self, url=Defaults.BASE_URL, api_key=None):
        """
        Initializes new Pyrai Object

        Args:
            url (str, optional): The base url for API calls. Defaults to Defaults.BASE_URL.
            api_key (str, optional): The API key. Defaults to None.
        """ 

        self.api_key = api_key
        self.base_url = url

    from pyrai.helpers import build_url

    def todict(self):
        """
        Converts the Pyrai object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """

        return {
            'api_key': self.api_key,
            'base_url': self.base_url
        }

    def __str__(self):
        return str(self.todict())

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
            return Fleet(api_key=self.api_key, fleet_key=resp.get('fleet_key'), params=params, base_url=self.base_url)
        else:
            raise StatusError(resp=resp)

    def create_sim_fleet(
        self, max_wait="3m", max_delay="6m",
        unlocked_window="2m", close_pickup_window="1s"
    ):
        """
        Creates a new simulation fleet.

        Args:
            max_wait (str, optional): The max wait time. Defaults to "3m".
            max_delay (str, optional): The max delay time. Defaults to "6m".
            unlocked_window (str, optional): The unlocked window time. Defaults to "2m".
            close_pickup_window (str, optional): The close pickup window time. Defaults to "1s".

        Returns:
            Fleet: The newly created fleet, if successful.

        Raises:
            StatusError: If the API call does not return a 200 response.
        """

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
        """
        Creates a new live fleet.

        Args:
            max_wait (str, optional): The max wait time. Defaults to "3m".
            max_delay (str, optional): The max delay time. Defaults to "6m".
            unlocked_window (str, optional): The unlocked window time. Defaults to "2m".
            close_pickup_window (str, optional): The close pickup window time. Defaults to "1s".

        Returns:
            Fleet: The newly created fleet, if successful.

        Raises:
            StatusError: If the API call does not return a 200 response.
        """

        return self.__create_fleet(
            Endpoints.CREATE_LIVE_FLEET,
            max_wait=max_wait,
            max_delay=max_delay,
            unlocked_window=unlocked_window,
            close_pickup_window=close_pickup_window,
        )
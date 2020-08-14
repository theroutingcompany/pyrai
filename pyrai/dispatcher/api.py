import urllib.parse
import requests
import datetime
import json
import IPython
import plotly.graph_objects as go
from dateutil.parser import isoparse
from pytimeparse.timeparse import timeparse
from .structures import *
from pyrai.helpers import to_rfc3339

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
    
    def build_url(self, endpoint):
        """
        Builds a URL given an endpoint

        Args:
            endpoint (Endpoint: str): The endpoint to build the URL for 

        Returns:
            str: The URL to access the given API endpoint
        """

        return urllib.parse.urljoin(self.base_url, endpoint)

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
            return Fleet(pyrai=self, fleet_key=resp.get('fleet_key'), params=params)
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
        fleet_key, 
        params=Defaults.DEFAULT_PARAMS, 
        api_key=None, 
        pyrai=None, 
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

        if api_key is None:
            api_key = pyrai.api_key

        if pyrai is None:
            pyrai = Pyrai(api_key=api_key, url=base_url)

        self.api_key = api_key
        self.fleet_key = fleet_key
        self.pyrai = pyrai
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

    def build_url(self, endpoint):
        """
        Builds a URL given an endpoint.

        Args:
            endpoint (Endpoint: str): The endpoint to build the URL for. 

        Returns:
            str: The URL to access the given API endpoint.
        """

        return self.pyrai.build_url(endpoint)

    def set_params(self,
        max_wait=None,
        max_delay=None,
        unlocked_window=None,
        close_pickup_window=None):
        """
        Mutates the fleet object and sets the provided params.

        Args:
            max_wait (str, optional): The max wait time. Defaults to None.
            max_delay (str, optional): The max delay time. Defaults to None.
            unlocked_window (str, optional): The unlocked window time. Defaults to None.
            close_pickup_window (str, optional): The close pickup window time. Defaults to None.

        Returns:
            StatusResponse: If successful.

        Raises:
            StatusError: If unsuccessful.
        """

        if max_wait is not None:
            self.params.max_wait = max_wait

        if max_delay is not None:
            self.params.max_delay = max_delay

        if unlocked_window is not None:
            self.params.unlocked_window = unlocked_window

        if close_pickup_window is not None:
            self.params.close_pickup_window = close_pickup_window

        url = self.build_url(Endpoints.SET_PARAMS)
        payload = {
            "params": self.params.todict(),
            "user_key": self.user_key.todict()
        }
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()
        
        if r.status_code == 200:
            return StatusResponse(resp=resp)
        else:
            raise StatusError(resp=resp)

    from pyrai.dispatcher.api_calls.fleet import make_vehicle_online, make_vehicle_offline, update_vehicle, remove_vehicle, get_vehicle_info
   
    
    def add_request(self, rid, pickup, dropoff, load, request_time=None):
        """
        Attempts to add a request.

        Args:
            rid (int): The unique request ID.
            pickup (Location): The pickup location.
            dropoff (Location): The dropoff location.
            load (int): The load (number of passengers).
            request_time (datetime.datetime, optional): Time of the request. This may be in the future for scheduled pickups. Set to datetime.datetime.now() if not provided. Defaults to None.

        Returns:
            StatusResponse: If successful.

        Raises:
            StatusError: If unsuccessful.
        """
        
        if request_time is None:
            request_time = datetime.datetime.now()

        if request_time > self.end_time:
            self.end_time = request_time

        url = self.build_url(Endpoints.ADD_REQUEST)
        payload = {
            'id': rid,
            'pickup': pickup.todict(),
            'dropoff': dropoff.todict(),
            'load': load,
            'request_time': to_rfc3339(request_time),
            'user_key': self.user_key.todict()
        }

        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return StatusResponse(resp=resp)
        else:
            raise StatusError(resp=resp)

    def cancel_request(self, rid, event_time=None):
        """
        Attempts to cancel a request.

        Args:
            rid (int): The unique request ID
            event_time (datetime.datetime, optional): Time of the cancellation. Set to datetime.datetime.now() if not provided. Defaults to None.

        Raises:
            StatusError: If unsuccessful.

        Returns:
            Status Response: If the request is sucessfully cancelled.
        """
        if event_time is None:
            event_time = datetime.datetime.now()

        if event_time > self.end_time:
            self.end_time = event_time

        url = self.build_url(Endpoints.CANCEL_REQUEST)
        payload = {
            'id': rid,
            'event_time': to_rfc3339(event_time),
            'user_key': self.user_key.todict()
        }

        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()
        
        if r.status_code == 200:
            return StatusResponse(resp=resp)
        else:
            raise StatusError(resp=resp)

    def get_request(self, rid):
        """
        Allows user to query request with given ID.

        Args:
            rid (int): The unique request ID.

        Raises:
            StatusError: If unsuccessful.

        Returns:
            Request: A request object representing the request with ID rid.
        """
        url = self.build_url(Endpoints.GET_REQUEST)
        payload = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
            'id': rid
        }

        r = requests.get(url, params=payload)
        resp = r.json()
        
        if r.status_code == 200:
            return Request.fromdict(self, resp)
        else:
            raise StatusError(resp=resp) 


    def get_assignments(self, current_time=None):
        """
        Computes vehicle assignments for the fleet in the current state.

        Args:
            current_time (datetime.datetime, optional): Current time. Set to datetime.datetime.now() if not provided. Defaults to None.

        Raises:
            StatusError: If unsuccessful.

        Returns:
            VehicleAssignments: If assignments are successfully computed.
        """
        if current_time is None:
            current_time = datetime.datetime.now()

        if current_time > self.end_time:
            self.end_time = current_time

        url = self.build_url(Endpoints.COMPUTE_ASSIGNMENTS)
        payload = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
            'current_time': to_rfc3339(current_time)
        }

        r = requests.get(url, params=payload)
        resp = r.json()

        if r.status_code == 200:
            return VehicleAssignments(
                vehs=[Vehicle.fromdict(self, veh) for veh in resp.get('vehs')],
                requests=[Request.fromdict(self, req) for req in resp.get('reqs')],
                notifications=[Notification.fromdict(notif) for notif in resp.get('notifications')],
            )
        else:
            raise StatusError(resp = resp)

    def forward_simulate(self, duration, current_time=None):
        """
        Forward simulates the fleet for a given duration.

        Args:
            duration (string): A duration to forward simulate for, e.g. "5m."
            current_time (datetime.datetime or str, optional): The current time, from when the simulation will begin. Can be provided as a datetime.datetime object or ISO string. Set to datetime.datetime.now() if not provided. Defaults to None.

        Returns:
            VehicleAssignments: The final state of all vehicles and requests, after the simulation.

        Raises:
            StatusError: If unsuccessful.
        """
        if current_time is None:
            current_time = datetime.datetime.now()

        if isinstance(current_time, str):
            current_time = isoparse(current_time)

        duration_td = datetime.timedelta(seconds=timeparse(duration))
    
        if current_time + duration_td > self.end_time:
            self.end_time = current_time + duration_td

        url = self.build_url(Endpoints.FORWARD_SIMULATE)
        payload = {
            'user_key': self.user_key.todict(),
            'sim_duration': duration,
            'current_time': to_rfc3339(current_time)
        }

        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return VehicleAssignments(
                vehs=[Vehicle.fromdict(self, veh) for veh in resp.get('vehs')],
                requests=[Request.fromdict(self, req) for req in resp.get('reqs')],
                notifications=[Notification.fromdict(notif) for notif in resp.get('notifications')],
            )
        else:
            raise StatusError(resp = resp)

        

    def visualize(self, start_time=None, end_time=None):
        """
        Visualizes the fleet for the given time frame.

        Args:
            start_time (datetime.datetime or str): The start time, either as a datetime.datetime object or an ISO string. Set to the python fleet creation time if not set. Defaults to None.
            end_time (datetime.datetime or str): The end time, either as a datetime.datetime object or an ISO string. Set to the latest API call time if not set. Defaults to None.

        Returns:
            IFrame: A graphic view of the fleet through time.
        """
        if start_time is None:
            start_time = self.start_time
        
        if end_time is None:
            end_time = self.end_time

        if isinstance(start_time, str):
            start_time = isoparse(start_time)

        if isinstance(end_time, str):
            end_time = isoparse(end_time)

        url = self.vis_url.format( 
            start = to_rfc3339(start_time), 
            end = to_rfc3339(end_time), 
            api_key = self.api_key, 
            fleet_key = self.fleet_key)

        print(url)

        return IPython.display.IFrame(url, 800, 800)

    def plot_metrics(self, metrics, start_time=None, end_time=None):
        """
        Plots time series metrics.

        Args:
            metrics (list[Metrics]): A list of metrics to plot.
            start_time (datetime.datetime or str): The start time, either as a datetime.datetime object or an ISO string. Set to the fleet creation time if not set. Defaults to None.
            end_time (datetime.datetime or str): The end time, either as a datetime.datetime object or an ISO string. Set to the latest API call time if not set. Defaults to None.

        Returns:
            Plotly.Figure: A figure that graphs the metrics
                over the time interval.
        """
        if start_time is None:
            start_time = self.start_time
        
        if end_time is None:
            end_time = self.end_time

        if isinstance(start_time, str):
            start_time = isoparse(start_time)

        if isinstance(end_time, str):
            end_time = isoparse(end_time)

        url = self.build_url(Endpoints.GRAPHQL)
        query = Metrics.QUERY.format(
            api_key = self.api_key,
            fleet_key = self.fleet_key,
            start_time = to_rfc3339(start_time),
            end_time = to_rfc3339(end_time)
        )
        r = requests.post(url, json={"query": query})
        resp = r.json()
        data = resp['data']['live_fleets'][0]['metrics']
        x = [met[Metrics.TIME] for met in data]
        figure = go.Figure()
        for metric in metrics:
            figure.add_trace(go.Scatter(x=x, y=[met[metric] for met in data],
                        mode='lines+markers',
                        name=metric))
        return figure
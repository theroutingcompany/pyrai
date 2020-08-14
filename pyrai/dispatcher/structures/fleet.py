from ..structures import Defaults, Endpoints, StatusError, StatusResponse, Metrics, UserKey, Request, VehicleAssignments, Vehicle, Notification, Pyrai
import datetime
from dateutil.parser import isoparse
import requests
import json
from pyrai.helpers import to_rfc3339
import IPython
import plotly.graph_objects as go
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

    from pyrai.dispatcher.api_calls.fleet import make_vehicle_online, make_vehicle_offline, update_vehicle, remove_vehicle, get_vehicle_info, set_params, add_request, cancel_request, get_request, get_assignments

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
import urllib.parse
import requests
import datetime
import json
import IPython
import plotly.graph_objects as go
from dateutil.parser import isoparse
from pytimeparse.timeparse import timeparse

class FleetParams(object):
    """
    Class used to set fleet parameters for simulations.

    Attributes:
        max_wait (str): The max wait time.
        max_delay (str): The max delay time.
        unlocked_window (str): The unlocked window time.
        close_pickup_window (str): The close pickup window time.
    """

    def __init__(self, max_wait, max_delay, unlocked_window, close_pickup_window):
        """
        Initializes a new FleetParams Object.

        Args:
            max_wait (str): The max wait time.
            max_delay (str): The max delay time.
            unlocked_window (str): The unlocked window time.
            close_pickup_window (str): The close pickup window time.
        """        

        self.max_wait = max_wait
        self.max_delay = max_delay
        self.unlocked_window = unlocked_window
        self.close_pickup_window = close_pickup_window

    def todict(self):
        """
        Converts the FleetParams object to a python dictionary.
        
        Returns:
            dict: A dictionary representation of self.
        """

        return {
            'max_wait': self.max_wait,
            'max_delay': self.max_delay,
            'unlocked_window': self.unlocked_window,
            'close_pickup_window': self.close_pickup_window
        }

class Defaults:
    """
    Class used to set default values for various parameters
    used by the API.
    """

    BASE_URL = "https://api.routable.ai"
    VISUALIZATION_URL = "https://dashboard.routable.ai/pyraimap?start={start}&end={end}&api_key={api_key}&fleet_key={fleet_key}"
    DEFAULT_CAPACITY = 6
    DEFAULT_DIRECTION = 0
    DEFAULT_PARAMS = FleetParams(
            max_wait="3m",
            max_delay="6m",
            unlocked_window="2m",
            close_pickup_window="1s"
        )


class StatusError(Exception):
    """
    Error raised for responses that are not 200s.

    Attributes:
        resp (dict): The response.
        status (int): The status of the response, should be nonzero
            if error is raised.
        error (string): Description of the error.
    """
    def __init__(self, resp=None, status=None, error=None):
        """
        Initializes a StatusError.

        Args:
            resp (dict, optional): The response. Defaults to None.
            status (int, optional): The status of the response, should
                be nonzero if error is raised. Defaults to None.
            error (string, optional): Description of the error. Defaults to None.
        """

        if resp is not None:
            self.status = resp.get('status')
            self.error = resp.get('error')
        else:
            self.status = status
            self.error = error

    def __str__(self):
        return self.error


class Endpoints:
    """
    Class used to specify API endpoints.
    """

    CREATE_SIM_FLEET = "/dispatcher/simulation/create"
    CREATE_LIVE_FLEET = "/dispatcher/live/create"
    MAKE_VEHICLE_ONLINE = "/dispatcher/vehicle/online"
    MAKE_VEHICLE_OFFLINE = "/dispatcher/vehicle/offline"
    UPDATE_VEHICLE = "/dispatcher/vehicle/update"
    REMOVE_VEHICLE = "/dispatcher/vehicle/remove"
    GET_VEHICLE_INFO = "/dispatcher/vehicle"
    ADD_REQUEST = "/dispatcher/request/add"
    GET_REQUEST = "/dispatcher/request"
    CANCEL_REQUEST = "/dispatcher/request/cancel"
    COMPUTE_ASSIGNMENTS = "/dispatcher/assignments"
    SET_PARAMS = "/dispatcher/params"
    FORWARD_SIMULATE = "/dispatcher/simulation/forward"
    GRAPHQL = "/graphql"


class Metrics:
    """
    Class used to specify the metrics that can be queried.
    """

    TIME = "time"
    PASSENGERS = "passengers"
    WAITING_REQUESTS = "waiting_requests"
    ACTIVE_REQUESTS = "active_requests"
    DROPPED_REQUESTS = "dropped_requests"
    CANCELED_REQUESTS = "canceled_requests"
    TOTAL_REQUESTS = "total_requests"
    ASSIGNED_VEHICLES = "assigned_vehicles"
    IDLE_VEHICLES = "idle_vehicles"
    REBALANCING_VEHICLES = "rebalancing_vehicles"
    OFFLINE_VEHICLES = "offline_vehicles"
    AVG_WAIT = "avg_wait"
    AVG_DELAY = "avg_delay"
    AVG_OCCUPANCY = "avg_occupancy"
    SERVICE_RATE = "service_rate"
    QUERY = """
    {{
    live_fleets(
        api_key: "{api_key}"
        fleet_key: "{fleet_key}"
    ) {{
        metrics (
        start: "{start_time}"
        end: "{end_time}"
        ) {{
            time
            passengers
            waiting_requests
            active_requests
            dropped_requests
            canceled_requests
            total_requests
            assigned_vehicles
            idle_vehicles
            rebalancing_vehicles
            offline_vehicles
            avg_wait
            avg_delay
            avg_occupancy
            service_rate
            }}
        }}
    }}
    """

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
    
    def make_vehicle_online(self, vid, location, capacity):
        """
        Attempts to make vehicle online.

        Args:
            vid (int): The vehicle ID.
            location (Location): The vehicle location.
            capacity (int): The vehicle capacity.

        Raises:
            StatusError: If unsuccessful.

        Returns:
            StatusReponse: If successful.
        """

        if datetime.datetime.now() > self.end_time:
            self.end_time = datetime.datetime.now()

        url = self.build_url(Endpoints.MAKE_VEHICLE_ONLINE)
        payload = {
            "location": location.todict(),
            "id": vid,
            'capacity': capacity,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data=json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return StatusResponse(resp=resp)
        else:
            raise StatusError(resp=resp)
        
    def make_vehicle_offline(self, vid, location):
        """
        Attempts to take vehicle offline.

        Args:
            vid (int): The vehicle ID.
            location (Location): The vehicle location.

        Raises:
            StatusError: If unsuccessful.

        Returns:
            StatusReponse: If successful.
        """
        if datetime.datetime.now() > self.end_time:
            self.end_time = datetime.datetime.now()

        url = self.build_url(Endpoints.MAKE_VEHICLE_OFFLINE)
        payload = {
            'location': location.todict(),
            'id': vid,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()
        
        if r.status_code == 200:
            return StatusResponse(resp=resp)
        else:
            raise StatusError(resp=resp)
    
    def update_vehicle(self, vid, location, event, direction=Defaults.DEFAULT_DIRECTION, event_time=None, req_id=None):
        """
        Attempts to update a vehicle.

        Args:
            vid (int): The unique vehicle ID
            location (Location): The vehicle location.
            direction (float): Angle in radians clockwise away from true north
            event (VehicleEvent): Describes the current event for the vehicle. 
                pickup occurs when the vehicle has picked up a request. 
                dropoff occurs when the vehicle has dropped of a request. 
                progress should be set when the vehicle is moving to service a request, 
                either picking up or dropping off. The vehicle should be marked as 
                unassigned when it is is not assigned to any requests.
            event_time (datetime.datetime, optional): Time at which the vehicle update has occurred. 
                Set to datetime.datetime.now() if not provided. Defaults to None.
            req_id (int, optional): The unique ID of request the vehicle is servicing. 
                If the vehicle is unassigned, this may be omitted. Defaults to None.

        Returns:
            Vehicle: If successful.

        Raises:
            StatusError: If unsucessful.
        """
        if event_time is None:
            event_time = datetime.datetime.now()

        if event_time > self.end_time:
            self.end_time = event_time

        url = self.build_url(Endpoints.UPDATE_VEHICLE)
        payload = {
            'id': vid,
            'location': location.todict(),
            'direction': direction,
            'event_time': to_rfc3339(event_time),
            'event': event,
            'user_key': self.user_key.todict()
        }
        
        if req_id is not None:
            payload['req_id'] = req_id
        
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            return Vehicle.fromdict(self, resp)
        else:
            raise StatusError(resp = resp)

    def remove_vehicle(self, vid, location):
        """
        Attempts to remove a vehicle.

        Args:
            vid (int): The unique vehicle ID.
            location (Location): The vehicle Location.

        Returns:
            list[int]: If vehicle is successfully removed, returns
                a list of IDs of passengers of the vehicle.

        Raises:
            StatusError: If unsuccessful.
        """

        if datetime.datetime.now() > self.end_time:
            self.end_time = datetime.datetime.now()
        
        url = self.build_url(Endpoints.REMOVE_VEHICLE)
        payload = {
            'location': location.todict(),
            'id': vid,
            'user_key': self.user_key.todict()
        }
        r = requests.post(url, data = json.dumps(payload))
        resp = r.json()

        if r.status_code == 200:
            if resp is not None:
                return resp.get('req_ids')
            else:
                return []
        else:
            raise StatusError(resp = resp)
            
    # need to update to use GraphQL but the endpoint doesn't work as expected
    def get_vehicle_info(self, vid):
        """
        Attempts to get vehicle info.

        Args:
            vid (int): The unique vehicle ID.

        Raises:
            StatusError: If unsuccessful.

        Returns:
            Vehicle: If succesful, returns a vehicle object corresponding to the
                vehicle with ID vid.
        """
        url = self.build_url(Endpoints.GET_VEHICLE_INFO)
        params = {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key,
            'id': vid
        }
        r = requests.get(url, params = params)
        resp = r.json()

        if r.status_code == 200:
            return Vehicle.fromdict(self, resp)
        else:
            raise StatusError(resp=resp) 
    
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
        


def to_rfc3339(dt):
    """
    Converts datetime objects to RFC3339 string for use with the API.

    Args:
        dt (datetime.datetime): A datetime.datetime object.

    Returns:
        string: An RFC3339 representation of dt.
    """
    return dt.astimezone(datetime.timezone.utc).isoformat()[:-6] + "Z"

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


class UserKey(object):
    """
    Class for representing user keys.

    Attributes:
        api_key (string): The API key.
        fleet_key (string): The fleet key.
    """
    def __init__(self, api_key, fleet_key):
        """
        Initializes a UserKey object.

        Args:
            api_key (string): The API key.
            fleet_key (string): The fleet key.
        """
        self.api_key = api_key
        self.fleet_key = fleet_key
    
    def todict(self):
        """
        Converts the UserKey object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'api_key': self.api_key,
            'fleet_key': self.fleet_key
        }

    def __str__(self):
        return str(self.todict())


class Location(object):
    """
    Class for representing locations.

    Attributes:
        lat (float): The latitude.
        lng (float): The longitude.
    """

    def __init__(self, lat, lng):
        """
        Initializes a location object

        Args:
            lat (float): The latitude.
            lng (float): The longitude.
        """

        self.lat = lat
        self.lng = lng
    
    @staticmethod
    def fromdict(d):
        """
        Converts a dict object into a Location object.

        Args:
            d (dict): The dictionary to convert.

        Returns:
            Location: A Location object with attributes set by
                fields in the dictionary.
        """
        return Location(d.get('lat'), d.get('lng'))

    def todict(self):
        """
        Converts a Location object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """

        return {
            'lat': self.lat,
            'lng': self.lng
        }

    def __str__(self):
        return str(self.todict())


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

class VehicleEvent:
    """
    Describes the current event for a vehicle. 
    `PICKUP` occurs when the vehicle has picked up a request. 
    `DROPOFF` occurs when the vehicle has dropped of a request. 
    `PROGRESS` should be set when the vehicle is moving to service a request, 
    either picking up or dropping off. 
    The vehicle should be marked as `UNASSIGNED` when it is is not 
    assigned to any requests.
    """
    PICKUP = "pickup"
    DROPOFF = "dropoff"
    PROGRESS = "progress"
    UNASSIGNED = "unassigned"

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

class Notification(object):
    """
    Class for representing notifications.

    Attributes:
        message (str): The notification message.
        data (NotificationData): the notification data.
    """
    def __init__(self, message, data):
        """
        Initializes a Notification object.

        Args:
            message (str): The notification message.
            data (NotificationData): the notification data.
        """
        self.message = message
        self.data = data
    
    @staticmethod
    def fromdict(d):
        """
        Converts python dictionary to Notification object.

        Args:
            d (dict): The dictionary to convert.

        Returns:
            Notification: a Notification object with attributes set by
                the values in d.
        """
        return Notification(
            d.get('message'),
            NotificationData.fromdict(d.get('data'))
        )

    def todict(self):
        """
        Converts a notification object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'message': self.message,
            'data': self.data.todict()
        }

    def __str__(self):
        return str(self.todict())

class NotificationData(object):
    """
    Class used to represent notification data.

    Attributes:
        veh_id (int): The vehicle ID.
        req_id (int): The request ID.
        waiting_duration (str): The waiting duration.
        assigned (bool): True if assigned, false if not.
    """
    def __init__(self, veh_id, req_id, waiting_duration, assigned):
        """
        Initializes a NotificationData object.

        Args:
            veh_id (int): The vehicle ID.
            req_id (int): The request ID.
            waiting_duration (str): The waiting duration.
            assigned (bool): True if assigned, false if not.
        """
        self.veh_id = veh_id
        self.req_id = req_id
        self.waiting_duration = waiting_duration
        self.assigned = assigned

    @staticmethod
    def fromdict(d):
        """
        Converts a python dictionary to a NotificationData object.

        Args:
            d (dict): The dictionary to convert.

        Returns:
            NotificationData: A NotificationData object with the attributes
                set by values in d.
        """
        return NotificationData(
            d.get('veh_id'),
            d.get('req_id'),
            d.get('waiting_duration'),
            d.get('assigned')
        )

    def todict(self):
        """
        Converts a NotificationData object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """

        return {
            'veh_id': self.veh_id,
            'req_id': self.req_id,
            'waiting_duration': self.waiting_duration,
            'assigned': self.assigned
        }

    def __str__(self):
        return str(self.todict())

class StatusResponse(object):
    """
    Class used for representing Status Responses.

    Attributes:
        resp (dict): The response.
        status (int): The status of the response.
        error (string): Description of the error.

    """
    def __init__(self, resp=None, status=None, error=None):
        """
        Initializes a StatusResponse Object

        Args:
            resp (dict, optional): The response. Defaults to None.
            status (int, optional): The status of the response. Defaults to None.
            error (str, optional): Description of the error. Defaults to None.
        """
        if resp is not None:
            self.status = resp.get('status')
            self.error = resp.get('error')
        else:
            self.status = status
            self.error = error

    def todict(self):
        """
        Converts StatusResponse object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'status': self.status,
            'error': self.error
        }

    def __str__(self):
        return str(self.todict())

    def __repr__(self):
        return "Success!"

class VehicleAssignments(object):
    """
    Class used to represent Vehicle Assignments.

    Attributes:
        vehs (list[Vehicle]): A list of vehicles in the fleet.
        requests (list[Request]): A list of requests in the fleet.
        notifications (list[Notification]): A list of notifications for the fleet.
    """
    def __init__(self, vehs=[], requests=[], notifications=[]):
        """
        Initializes a VehicleAssignments object.

        Args:
            vehs (list[Vehicle], optional): A list of vehicles in the fleet. Defaults to [].
            requests (list[Request], optional): A list of requests in the fleet. 
                Defaults to [].
            notifications (list[Notification], optional): A list of notifications 
                for the fleet. Defaults to [].
        """
        self.vehs = vehs
        self.requests = requests
        self.notifications = notifications

    def todict(self):
        """
        Converts VehicleAssignments object to python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'vehs': [v.todict() for v in self.vehs], 
            'requests': [r.todict() for r in self.requests],
            'notifications': [n.todict() for n in self.notifications]
        }

    def __str__(self):
        return str(self.todict())

    def __repr__(self):
        return str(self.todict())

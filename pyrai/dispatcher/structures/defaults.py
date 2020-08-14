from .fleet_params import FleetParams

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
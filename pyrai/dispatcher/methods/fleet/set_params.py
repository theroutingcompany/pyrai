import requests
import json
from pyrai.dispatcher.structures.endpoints import Endpoints
from pyrai.dispatcher.structures.status_response import StatusResponse
from pyrai.dispatcher.structures.status_error import StatusError

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
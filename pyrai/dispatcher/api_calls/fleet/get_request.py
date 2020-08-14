from pyrai.dispatcher.structures import Endpoints, Request, StatusError
import requests
import json

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

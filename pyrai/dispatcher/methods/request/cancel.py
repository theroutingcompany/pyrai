import datetime

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
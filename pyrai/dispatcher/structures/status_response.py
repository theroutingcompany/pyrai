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
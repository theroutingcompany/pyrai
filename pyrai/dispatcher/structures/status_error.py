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
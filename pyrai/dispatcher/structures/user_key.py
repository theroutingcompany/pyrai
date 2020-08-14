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
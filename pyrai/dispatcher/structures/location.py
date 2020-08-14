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
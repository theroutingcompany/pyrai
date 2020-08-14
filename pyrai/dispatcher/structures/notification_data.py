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
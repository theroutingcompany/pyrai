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

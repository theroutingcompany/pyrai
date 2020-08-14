class FleetParams(object):
    """
    Class used to set fleet parameters for simulations.

    Attributes:
        max_wait (str): The max wait time.
        max_delay (str): The max delay time.
        unlocked_window (str): The unlocked window time.
        close_pickup_window (str): The close pickup window time.
    """

    def __init__(self, max_wait, max_delay, unlocked_window, close_pickup_window):
        """
        Initializes a new FleetParams Object.

        Args:
            max_wait (str): The max wait time.
            max_delay (str): The max delay time.
            unlocked_window (str): The unlocked window time.
            close_pickup_window (str): The close pickup window time.
        """        

        self.max_wait = max_wait
        self.max_delay = max_delay
        self.unlocked_window = unlocked_window
        self.close_pickup_window = close_pickup_window

    def todict(self):
        """
        Converts the FleetParams object to a python dictionary.
        
        Returns:
            dict: A dictionary representation of self.
        """

        return {
            'max_wait': self.max_wait,
            'max_delay': self.max_delay,
            'unlocked_window': self.unlocked_window,
            'close_pickup_window': self.close_pickup_window
        }
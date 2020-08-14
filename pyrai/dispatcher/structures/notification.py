from .notification_data import NotificationData

class Notification(object):
    """
    Class for representing notifications.

    Attributes:
        message (str): The notification message.
        data (NotificationData): the notification data.
    """
    def __init__(self, message, data):
        """
        Initializes a Notification object.

        Args:
            message (str): The notification message.
            data (NotificationData): the notification data.
        """
        self.message = message
        self.data = data
    
    @staticmethod
    def fromdict(d):
        """
        Converts python dictionary to Notification object.

        Args:
            d (dict): The dictionary to convert.

        Returns:
            Notification: a Notification object with attributes set by
                the values in d.
        """
        return Notification(
            d.get('message'),
            NotificationData.fromdict(d.get('data'))
        )

    def todict(self):
        """
        Converts a notification object to a python dictionary.

        Returns:
            dict: A dictionary representation of self.
        """
        return {
            'message': self.message,
            'data': self.data.todict()
        }

    def __str__(self):
        return str(self.todict())
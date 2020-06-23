class StatusResponse():
    def __init__(self, status, error):
        self.status = status
        self.error = error

    def __str__(self):
        return str(self.__dict__)
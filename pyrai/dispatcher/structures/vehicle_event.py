class VehicleEvent:
    """
    Describes the current event for a vehicle. 
    `PICKUP` occurs when the vehicle has picked up a request. 
    `DROPOFF` occurs when the vehicle has dropped of a request. 
    `PROGRESS` should be set when the vehicle is moving to service a request, 
    either picking up or dropping off. 
    The vehicle should be marked as `UNASSIGNED` when it is is not 
    assigned to any requests.
    """
    PICKUP = "pickup"
    DROPOFF = "dropoff"
    PROGRESS = "progress"
    UNASSIGNED = "unassigned"
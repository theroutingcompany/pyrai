class Endpoints:
    """
    Class used to specify API endpoints.
    """

    CREATE_SIM_FLEET = "/dispatcher/simulation/create"
    CREATE_LIVE_FLEET = "/dispatcher/live/create"
    MAKE_VEHICLE_ONLINE = "/dispatcher/vehicle/online"
    MAKE_VEHICLE_OFFLINE = "/dispatcher/vehicle/offline"
    UPDATE_VEHICLE = "/dispatcher/vehicle/update"
    REMOVE_VEHICLE = "/dispatcher/vehicle/remove"
    GET_VEHICLE_INFO = "/dispatcher/vehicle"
    ADD_REQUEST = "/dispatcher/request/add"
    GET_REQUEST = "/dispatcher/request"
    CANCEL_REQUEST = "/dispatcher/request/cancel"
    COMPUTE_ASSIGNMENTS = "/dispatcher/assignments"
    SET_PARAMS = "/dispatcher/params"
    FORWARD_SIMULATE = "/dispatcher/simulation/forward"
    GRAPHQL = "/graphql"

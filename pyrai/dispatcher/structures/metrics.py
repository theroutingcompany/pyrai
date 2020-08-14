class Metrics:
    """
    Class used to specify the metrics that can be queried.
    """

    TIME = "time"
    PASSENGERS = "passengers"
    WAITING_REQUESTS = "waiting_requests"
    ACTIVE_REQUESTS = "active_requests"
    DROPPED_REQUESTS = "dropped_requests"
    CANCELED_REQUESTS = "canceled_requests"
    TOTAL_REQUESTS = "total_requests"
    ASSIGNED_VEHICLES = "assigned_vehicles"
    IDLE_VEHICLES = "idle_vehicles"
    REBALANCING_VEHICLES = "rebalancing_vehicles"
    OFFLINE_VEHICLES = "offline_vehicles"
    AVG_WAIT = "avg_wait"
    AVG_DELAY = "avg_delay"
    AVG_OCCUPANCY = "avg_occupancy"
    SERVICE_RATE = "service_rate"
    QUERY = """
    {{
    live_fleets(
        api_key: "{api_key}"
        fleet_key: "{fleet_key}"
    ) {{
        metrics (
        start: "{start_time}"
        end: "{end_time}"
        ) {{
            time
            passengers
            waiting_requests
            active_requests
            dropped_requests
            canceled_requests
            total_requests
            assigned_vehicles
            idle_vehicles
            rebalancing_vehicles
            offline_vehicles
            avg_wait
            avg_delay
            avg_occupancy
            service_rate
            }}
        }}
    }}
    """
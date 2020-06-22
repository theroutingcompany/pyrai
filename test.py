import requests
import json
from structures import *
from all_api_calls import *
from request_query import *

test_params = structures.FleetParams("5m30s", "10m", "2m", "30s")

if __name__ == '__main__':
    r = RequestQuery("774721b6-2e77-4d4a-8b4c-e997bcef11c3")
    r1 = r.create_simulated_fleet(test_params)
    print(r1)
    r.set_fleet_key(r1["fleet_key"])
    r2 = r.compute_assignments()
    print(r2)
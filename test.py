import requests
import json
from source import *

API_KEY = "774721b6-2e77-4d4a-8b4c-e997bcef11c3"
test_params = structures.FleetParams("5m30s", "10m", "2m", "30s")

if __name__ == '__main__':
    # r = RequestQuery("774721b6-2e77-4d4a-8b4c-e997bcef11c3")
    # r1 = r.create_simulated_fleet(test_params)
    # print(r1)
    # r.set_fleet_key(r1["fleet_key"])
    # r2 = r.compute_assignments()
    # print(r2)

    # create fleet
    query = create_simulated_fleet.CreateSimulatedFleetQuery(API_KEY, test_params)
    r1 = query.run()
    print(r1)

    # set/change params
    new_params = structures.FleetParams("5m", "5m", "2m", "30s")
    user_key = structures.UserKey(API_KEY, r1.fleet_key)
    query = set_params.SetParamsQuery(new_params, user_key)
    r2 = query.run()
    print(r2)

    # make vehicle online

    # add request

    # update vehicle

    # get vehicle info

    # get request info

    # compute assignment

    # make vehicle offline

    # remove vehicle

    # cancel request

    # query historical state
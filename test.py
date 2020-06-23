import requests
import json
import datetime
from source import *

API_KEY = "774721b6-2e77-4d4a-8b4c-e997bcef11c3"
test_params = structures.FleetParams("5m30s", "10m", "2m", "30s")

if __name__ == '__main__':

    # create fleet
    query = create_simulated_fleet.CreateSimulatedFleetQuery(API_KEY, test_params)
    r1 = query.run()
    print(r1)

    # set/change params
    new_params = structures.FleetParams("5m", "5m", "2m", "30s")
    USER_KEY = structures.UserKey(API_KEY, r1.fleet_key)
    query = set_params.SetParamsQuery(new_params, USER_KEY)
    r2 = query.run()
    print(r2)

    # make vehicle online
    location = structures.Location(40.75466940037548, -73.99382114410399)
    id = 42
    capacity = 4
    query = make_vehicle_online.MakeVehicleOnlineQuery(location, id, capacity, USER_KEY)
    r3 = query.run()
    print(r3)

    # add request
    pickup = structures.Location(40.76466940037548, -73.98382114410399)
    dropoff = structures.Location(40.74465591168391, -73.98643970489502)
    id = 30
    load = 2
    query = add_request.AddRequestQuery(id, pickup, dropoff, load, datetime.datetime.now(), USER_KEY)
    r4 = query.run()
    print(r4)

    # compute assignment
    query = compute_assignments.ComputeAssignmentsQuery(API_KEY, USER_KEY.fleet_key)
    r5 = query.run()
    print(r5)

    # update vehicle
    id = 42
    location = structures.Location(40.75466940037548, -73.98382114410399)
    direction = 1.02
    event_time = datetime.datetime.now()
    req_id = 30
    event = "progress"
    query = update_vehicle.UpdateVehicleQuery(id, location, direction, event_time, req_id, event, USER_KEY)
    r6 = query.run()
    print(r6)

    # get vehicle info
    query = get_vehicle_info.GetVehicleInfoQuery(API_KEY, USER_KEY.fleet_key, 42)
    r7=query.run()
    print(r7)

    # get request info

    # make vehicle offline

    # remove vehicle

    # cancel request

    # query historical state
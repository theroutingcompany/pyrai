import unittest
import datetime
from pyrai.api import *

class TestAPICalls(unittest.TestCase):

    bad_api_key = "abcd"
    api_key = "774721b6-2e77-4d4a-8b4c-e997bcef11c3"

    def test_create_and_destroy(self):
        rai = Pyrai(api_key=self.api_key)
        self.assertEqual(rai.api_key, self.api_key)
        bad_rai = Pyrai(api_key=self.bad_api_key)
        self.assertEqual(bad_rai.api_key, self.bad_api_key)

        # sim fleet
        sim_fleet = rai.create_sim_fleet(max_wait="3m", max_delay="6m",
            unlocked_window="2m", close_pickup_window="1s")
        self.assertEqual(sim_fleet.api_key, self.api_key)
        self.assertIsNotNone(sim_fleet.fleet_key)
        self.assertEqual(sim_fleet.pyrai, rai)
        with self.assertRaises(StatusError):
            bad_rai.create_sim_fleet()

        # live fleet
        live_fleet = rai.create_live_fleet(max_wait="3m", max_delay="6m",
            unlocked_window="2m", close_pickup_window="1s")
        self.assertEqual(live_fleet.api_key, self.api_key)
        self.assertIsNotNone(live_fleet.fleet_key)
        self.assertEqual(live_fleet.pyrai, rai)
        with self.assertRaises(StatusError):
            bad_rai.create_live_fleet()

        # make vehicle online
        resp = sim_fleet.make_vehicle_online(1, Location(80, -80), 5)
        self.assertEqual(resp.status, 0, resp.error)
    
        # get vehicle info
        veh = sim_fleet.get_vehicle_info(1)
        self.assertEqual(veh.fleet, sim_fleet)
        self.assertEqual(veh.veh_id, 1)

        # update loc
        old_loc = veh.location
        veh.update(VehicleEvent.UNASSIGNED, location=Location(50.75, 6.01))
        self.assertEqual(veh.fleet, sim_fleet)
        self.assertEqual(veh.veh_id, 1)
        self.assertNotEqual(veh.location, old_loc)

        # add request
        resp = sim_fleet.add_request(2, 
            Location(50.75, 6.019), 
            Location(51.15, 6.017), 
            3, 
            datetime.datetime.now())
        self.assertEqual(resp.status, 0, resp.error)

        # get request
        req = sim_fleet.get_request(2)
        self.assertEqual(req.fleet, sim_fleet)
        self.assertEqual(req.veh_id, -1)
        self.assertEqual(req.req_id, 2)
        self.assertEqual(req.load, 3)
        self.assertEqual(req.assigned, False)

        # set params
        resp = sim_fleet.set_params(
            max_wait="4m", max_delay="8m",
            unlocked_window="3m", close_pickup_window="2s"
        )
        self.assertEqual(resp.status, 0, resp.error)

        # get assignments
        assignments = sim_fleet.get_assignments(datetime.datetime.now())
        self.assertEqual(len(assignments.vehs), 1)
        self.assertEqual(len(assignments.requests), 1)
        self.assertEqual(assignments.vehs[0].veh_id, 1)
        self.assertEqual(assignments.requests[0].req_id, 2)

        # cancel request
        resp = sim_fleet.cancel_request(2, datetime.datetime.now())
        self.assertEqual(resp.status, 0, resp.error)

        # make vehicle offline
        resp = veh.make_offline()
        self.assertEqual(resp.status, 0, resp.error)

        # remove vehicle
        resp = veh.remove()
        self.assertEqual(resp, None)

if __name__ == '__main__':
    unittest.main()
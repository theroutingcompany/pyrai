import unittest
import datetime
from pyrai.api import *

class TestAPICalls(unittest.TestCase):

    bad_api_key = "abcd"
    api_key = "774721b6-2e77-4d4a-8b4c-e997bcef11c3"

    def test_create_pyrai(self):
        TestAPICalls.rai = Pyrai(api_key=self.api_key)
        self.assertEqual(self.rai.api_key, self.api_key)
        TestAPICalls.bad_rai = Pyrai(api_key=self.bad_api_key)
        self.assertEqual(self.bad_rai.api_key, self.bad_api_key)

    def test_create_sim_fleet(self):
        TestAPICalls.sim_fleet = self.rai.create_sim_fleet(max_wait="3m", max_delay="6m",
            unlocked_window="2m", close_pickup_window="1s")
        self.assertEqual(self.sim_fleet.api_key, self.api_key)
        self.assertIsNotNone(self.sim_fleet.fleet_key)
        self.assertEqual(self.sim_fleet.pyrai, self.rai)
        with self.assertRaises(StatusError):
            self.bad_rai.create_sim_fleet()

    def test_create_live_fleet(self):
        TestAPICalls.live_fleet = self.rai.create_live_fleet(max_wait="3m", max_delay="6m",
            unlocked_window="2m", close_pickup_window="1s")
        self.assertEqual(self.live_fleet.api_key, self.api_key)
        self.assertIsNotNone(self.live_fleet.fleet_key)
        self.assertEqual(self.live_fleet.pyrai, self.rai)
        with self.assertRaises(StatusError):
            self.bad_rai.create_live_fleet()

    def test_make_vehicle_online(self):
        resp = self.sim_fleet.make_vehicle_online(1, Location(80, -80), 5)
        self.assertEqual(resp.status, 0, resp.error)
    
    def test_get_vehicle_info(self):
        TestAPICalls.veh = self.sim_fleet.get_vehicle_info(1)
        self.assertEqual(self.veh.fleet, self.sim_fleet)
        self.assertEqual(self.veh.veh_id, 1)

    def test_update_vehicle(self):
        old_loc = self.veh.location
        self.veh.update(VehicleEvent.UNASSIGNED, location=Location(50.75, 6.01))
        self.assertEqual(self.veh.fleet, self.sim_fleet)
        self.assertEqual(self.veh.veh_id, 1)
        self.assertNotEqual(self.veh.location, old_loc)

    def test_add_request(self):
        resp = self.sim_fleet.add_request(2, 
            Location(50.75, 6.019), 
            Location(51.15, 6.017), 
            3, 
            datetime.datetime.now())
        self.assertEqual(resp.status, 0, resp.error)

    def test_get_request(self):
        TestAPICalls.req = self.sim_fleet.get_request(2)
        self.assertEqual(self.req.fleet, self.sim_fleet)
        self.assertEqual(self.req.veh_id, -1)
        self.assertEqual(self.req.req_id, 2)
        self.assertEqual(self.req.load, 3)
        self.assertEqual(self.req.assigned, False)

    def test_set_params(self):
        resp = self.sim_fleet.set_params(
            max_wait="4m", max_delay="8m",
            unlocked_window="3m", close_pickup_window="2s"
        )
        self.assertEqual(resp.status, 0, resp.error)

    def test_get_assignments(self):
        TestAPICalls.assignments = self.sim_fleet.get_assignments(datetime.datetime.now())
        self.assertEqual(len(self.assignments.vehs), 1)
        self.assertEqual(len(self.assignments.requests), 1)
        self.assertEqual(self.assignments.vehs[0].veh_id, 1)
        self.assertEqual(self.assignments.requests[0].req_id, 2)

    def test_cancel_request(self):
        resp = self.sim_fleet.cancel_request(2, datetime.datetime.now())
        self.assertEqual(resp.status, 0, resp.error)

    def test_make_vehicle_offline(self):
        resp = self.veh.make_offline()
        self.assertEqual(resp.status, 0, resp.error)

    def test_remove_vehicle(self):
        resp = self.veh.remove()
        self.assertEqual(resp, None)


def suite(): # ensure the tests run in order
    suite = unittest.TestSuite()
    suite.addTest(TestAPICalls('test_create_pyrai'))
    suite.addTest(TestAPICalls('test_create_sim_fleet'))
    suite.addTest(TestAPICalls('test_create_live_fleet'))
    suite.addTest(TestAPICalls('test_make_vehicle_online'))
    suite.addTest(TestAPICalls('test_get_vehicle_info'))
    suite.addTest(TestAPICalls('test_update_vehicle'))
    suite.addTest(TestAPICalls('test_add_request'))
    suite.addTest(TestAPICalls('test_get_request'))
    suite.addTest(TestAPICalls('test_set_params'))
    suite.addTest(TestAPICalls('test_get_assignments'))
    suite.addTest(TestAPICalls('test_cancel_request'))
    suite.addTest(TestAPICalls('test_make_vehicle_offline'))
    suite.addTest(TestAPICalls('test_remove_vehicle'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
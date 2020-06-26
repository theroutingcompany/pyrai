import unittest
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
        TestAPICalls.bad_sim_fleet = self.bad_rai.create_sim_fleet()
        self.assertNotEqual(self.bad_sim_fleet.status, 0)

    def test_create_live_fleet(self):
        TestAPICalls.live_fleet = self.rai.create_live_fleet(max_wait="3m", max_delay="6m",
            unlocked_window="2m", close_pickup_window="1s")
        self.assertEqual(self.live_fleet.api_key, self.api_key)
        self.assertIsNotNone(self.live_fleet.fleet_key)
        self.assertEqual(self.live_fleet.pyrai, self.rai)
        TestAPICalls.bad_live_fleet = self.bad_rai.create_live_fleet()
        self.assertNotEqual(self.bad_live_fleet.status, 0)

    def test_make_vehicle_online(self):
        resp = self.sim_fleet.make_vehicle_online(1, Location(80, -80), 5)
        self.assertEqual(resp.status, 0)
    
    def test_get_vehicle_info(self):
        TestAPICalls.veh = self.sim_fleet.get_vehicle_info(1)
        self.assertEqual(self.veh.fleet, self.sim_fleet)
        self.assertEqual(self.veh.veh_id, 1)

    def test_update_vehicle(self):
        TestAPICalls.updated_veh = self.veh.update("unassigned", location=Location(50, 50))
        self.assertEqual(self.updated_veh.fleet, self.veh.fleet)
        self.assertEqual(self.updated_veh.veh_id, self.veh.veh_id)
        self.assertNotEqual(self.updated_veh.location, self.veh.location)

    def test_add_request(self):
        resp = self.sim_fleet.add_request(2, 
            Location(50, 7), 
            Location(51, 7), 
            3, 
            datetime.datetime.now())
        self.assertEqual(resp.status, 0)

    def test_get_request(self):
        TestAPICalls.req = self.sim_fleet.get_request(2)
        self.assertEqual(self.req.fleet, self.sim_fleet)
        self.assertEqual(self.req.veh_id, -1)
        self.assertEqual(self.req.req_id, 2)
        self.assertEqual(self.req.load, 3)
        self.assertEqual(self.req.assigned, False)


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
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
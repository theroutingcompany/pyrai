import unittest
from api import *

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
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAPICalls('test_create_pyrai'))
    suite.addTest(TestAPICalls('test_create_sim_fleet'))
    suite.addTest(TestAPICalls('test_create_live_fleet'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
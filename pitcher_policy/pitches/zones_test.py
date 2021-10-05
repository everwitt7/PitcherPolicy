"""ObviousZone Test Module"""
import unittest

from pitches.test_config import TEST_ZONES


class TestZonesClass(unittest.TestCase):
    """Test Zones class"""

    def setUp(self):
        self.zones = TEST_ZONES

    def test_in_strike_zone(self):
        """Test ObviousZone.in_strike_zone function"""
        self.assertTrue(self.zones.in_strike_zone(-1, 1))
        self.assertFalse(self.zones.in_strike_zone(-1, 4))

    def test_in_ball_zone(self):
        """Test ObviousZone.in_ball_zone function"""
        self.assertTrue(self.zones.in_ball_zone(-3.5, 3.5))
        self.assertFalse(self.zones.in_ball_zone(-5, -5))

    def test_in_obvious_zone(self):
        """Test ObviousZone.in_obvious_zone function"""
        self.assertFalse(self.zones.in_obvious_zone(0, 0))
        self.assertTrue(self.zones.in_obvious_zone(-3.5, 2.5))

    def test_return_zone(self):
        """Test ObviousZone.return_zone function"""
        self.assertEqual(self.zones.return_zone(-2, 2), "0a")
        self.assertEqual(self.zones.return_zone(0, 2), "1a")
        self.assertEqual(self.zones.return_zone(2, 2), "2a")
        self.assertEqual(self.zones.return_zone(-2, 0), "3a")
        self.assertEqual(self.zones.return_zone(0, 0), "4a")
        self.assertEqual(self.zones.return_zone(2, 0), "5a")
        self.assertEqual(self.zones.return_zone(-2, -2), "6a")
        self.assertEqual(self.zones.return_zone(0, -2), "7a")
        self.assertEqual(self.zones.return_zone(2, -2), "8a")

        self.assertEqual(self.zones.return_zone(-3.5, 3.5), "9a")
        self.assertEqual(self.zones.return_zone(0, 3.5), "10a")
        self.assertEqual(self.zones.return_zone(3.5, 3.5), "11a")
        self.assertEqual(self.zones.return_zone(-3.5, 0), "12a")
        self.assertEqual(self.zones.return_zone(3.5, 0), "13a")
        self.assertEqual(self.zones.return_zone(-3.5, -3.5), "14a")
        self.assertEqual(self.zones.return_zone(0, -3.5), "15a")
        self.assertEqual(self.zones.return_zone(3.5, -3.5), "16a")

        self.assertEqual(self.zones.return_zone(-5, 5), "9b")
        self.assertEqual(self.zones.return_zone(0, 5), "10b")
        self.assertEqual(self.zones.return_zone(5, 5), "11b")
        self.assertEqual(self.zones.return_zone(-3.5, 2.5), "12b")
        self.assertEqual(self.zones.return_zone(3.5, 2.5), "13b")
        self.assertEqual(self.zones.return_zone(-5, -5), "14b")
        self.assertEqual(self.zones.return_zone(0, -5), "15b")
        self.assertEqual(self.zones.return_zone(5, -5), "16b")


if __name__ == '__main__':
    unittest.main()

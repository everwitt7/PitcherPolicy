"""ObviousZone Test Module"""

import unittest

from pitchprediction.pitches.obvious_zones import ObviousZones


class TestObviousZonesClass(unittest.TestCase):
    """Test ObviousZone class"""

    def setUp(self):
        self.obvious_zones = ObviousZones(2, 3)

    def test_is_obvious(self):
        """Test ObviousZone.is_obvious function"""
        self.assertTrue(self.obvious_zones.is_obvious(8, -6))
        self.assertTrue(self.obvious_zones.is_obvious(1, 5))
        self.assertTrue(self.obvious_zones.is_obvious(-4, 2))
        self.assertFalse(self.obvious_zones.is_obvious(1, 1))

    def test_return_zone(self):
        """Test ObviousZone.return_zone function"""
        self.assertEqual(self.obvious_zones.return_zone(-3, 4), "9b")
        self.assertEqual(self.obvious_zones.return_zone(0, 4), "10b")
        self.assertEqual(self.obvious_zones.return_zone(3, 4), "11b")
        self.assertEqual(self.obvious_zones.return_zone(-3, 0), "12b")
        self.assertEqual(self.obvious_zones.return_zone(3, 0), "13b")
        self.assertEqual(self.obvious_zones.return_zone(-3, -4), "14b")
        self.assertEqual(self.obvious_zones.return_zone(0, -4), "15b")
        self.assertEqual(self.obvious_zones.return_zone(3, -4), "16b")
        self.assertEqual(self.obvious_zones.return_zone(0, 0), "-1")


if __name__ == '__main__':
    unittest.main()

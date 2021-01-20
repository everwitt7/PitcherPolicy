"""ObviousZone Test Module"""
import unittest

from zones import Zones, ObviousZones, Zone

LEFT_X = -3
MID_LEFT_X = -1
MID_RIGHT_X = 1
RIGHT_X = 3

TOP_Y = 3
MID_TOP_Y = 1
MID_BOT_Y = -1
BOT_Y = -3

test_strike_zone_inputs = {
    "0a": {
        "coords": (LEFT_X, MID_TOP_Y),
        "height": 2,
        "width": 2
    },
    "1a": {
        "coords": (MID_LEFT_X, MID_TOP_Y),
        "height": 2,
        "width": 2
    },
    "2a": {
        "coords": (MID_RIGHT_X, MID_TOP_Y),
        "height": 2,
        "width": 2
    },
    "3a": {
        "coords": (LEFT_X, MID_BOT_Y),
        "height": 2,
        "width": 2
    },
    "4a": {
        "coords": (MID_LEFT_X, MID_BOT_Y),
        "height": 2,
        "width": 2
    },
    "5a": {
        "coords": (MID_RIGHT_X, MID_BOT_Y),
        "height": 2,
        "width": 2
    },
    "6a": {
        "coords": (LEFT_X, BOT_Y),
        "height": 2,
        "width": 2
    },
    "7a": {
        "coords": (MID_LEFT_X, BOT_Y),
        "height": 2,
        "width": 2
    },
    "8a": {
        "coords": (MID_RIGHT_X, BOT_Y),
        "height": 2,
        "width": 2
    }
}
test_ball_zone_inputs = {
    "10a": {
        "coords": (LEFT_X, TOP_Y),
        "height": 1,
        "width": 6
    },
    "11a": {
        "coords": (RIGHT_X, TOP_Y),
        "height": 1,
        "width": 1
    },
    "13a": {
        "coords": (RIGHT_X, BOT_Y),
        "height": 5,
        "width": 1
    },
    "9a": {
        "coords": (-1+LEFT_X, TOP_Y),
        "height": 1,
        "width": 1
    },
    "12a": {
        "coords": (-1+LEFT_X, BOT_Y),
        "height": 5,
        "width": 1
    },
    "15a": {
        "coords": (LEFT_X, -1+BOT_Y),
        "height": 1,
        "width": 6
    },
    "16a": {
        "coords": (RIGHT_X, -1+BOT_Y),
        "height": 1,
        "width": 1
    },
    "14a": {
        "coords": (-1+LEFT_X, -1+BOT_Y),
        "height": 1,
        "width": 1
    }
}

# creating the data to instantiate a Zones object
test_obv_zones = ObviousZones(LEFT_X, TOP_Y)
test_strike_zone_list = list()
test_ball_zone_list = list()

for name, val in test_strike_zone_inputs.items():
    test_strike_zone_list.append(
        Zone(name, val["coords"], val["width"], val["height"]))

for name, val in test_ball_zone_inputs.items():
    test_ball_zone_list.append(
        Zone(name, val["coords"], val["width"], val["height"]))


class TestZonesClass(unittest.TestCase):
    """Test Zones class"""

    def setUp(self):
        self.zones = Zones(test_strike_zone_list,
                           test_ball_zone_list, test_obv_zones)

    def test_in_strike_zone(self):
        """Test ObviousZone.in_strike_zone() function"""
        self.assertTrue(self.zones.in_strike_zone(-1, 1))
        self.assertFalse(self.zones.in_strike_zone(-1, 4))

    def test_in_ball_zone(self):
        """Test ObviousZone.in_ball_zone() function"""
        self.assertTrue(self.zones.in_ball_zone(-3.5, 3.5))
        self.assertFalse(self.zones.in_ball_zone(-5, -5))

    def test_in_obvious_zone(self):
        """Test ObviousZone.in_obvious_zone() function"""
        self.assertFalse(self.zones.in_obvious_zone(0, 0))
        self.assertTrue(self.zones.in_obvious_zone(-3.5, 2.5))

    def test_return_zone(self):
        """Test ObviousZone.return_zone() function"""
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

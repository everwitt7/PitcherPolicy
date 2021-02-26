"""Zone Test Module"""

import unittest

from pitches.zone import Zone


class TestZoneClass(unittest.TestCase):
    """Test Zone class"""

    def setUp(self):
        self.zone = Zone("rectangle", (0, 0), 3, 5)

    def test_get_center(self):
        """Test Zone.get_center function"""
        self.assertEqual(self.zone.get_center(), (3/2, 5/2))

    def test_in_zone(self):
        """Test Zone.in_zone function"""
        self.assertTrue(self.zone.in_zone(2, 2))
        self.assertFalse(self.zone.in_zone(2, 6))
        self.assertFalse(self.zone.in_zone(-2, 2))
        self.assertFalse(self.zone.in_zone(4, -1))


if __name__ == '__main__':
    unittest.main()

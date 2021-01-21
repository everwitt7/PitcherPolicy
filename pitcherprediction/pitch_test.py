"""Pitch Test Module"""
import unittest

from pitch import Pitch
from pitch_zone_enums import PitchNames
from test_config import TEST_ERR_DIST, TEST_ZONES


class TestPitchClass(unittest.TestCase):
    """Test Pitch class"""

    def setUp(self):
        self.zones = Pitch(PitchNames.FOUR_SEEM.value,
                           TEST_ZONES, TEST_ERR_DIST)

    def test_run_error_simuation(self):
        """Test ObviousZone.in_strike_zone(trials) function"""


# TODO: make sure accuracy matrix sums to 1 - is that it?

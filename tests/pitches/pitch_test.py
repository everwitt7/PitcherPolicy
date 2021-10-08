"""Pitch Test Module"""
import unittest

from pitches.pitch import Pitch
from pitches.pitch_zone_enums import PitchNames
from pitches.test_config import TEST_ERR_DIST, TEST_ZONES


class TestPitchClass(unittest.TestCase):
    """Test Pitch class"""

    def setUp(self):
        self.pitch = Pitch(PitchNames.FOUR_SEAM.value,
                           TEST_ZONES, TEST_ERR_DIST)

    def test_run_error_simuation(self):
        """Test ObviousZone.in_strike_zone function"""
        acc_mat = self.pitch.run_error_simuation()
        for _, err in acc_mat.items():
            tot = sum([e for _, e in err.items()])
            self.assertAlmostEqual(1, tot, places=3)


if __name__ == '__main__':
    unittest.main()

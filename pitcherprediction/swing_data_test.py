"""SwingData Test Module"""
import unittest

from swing_data import SwingData

class TestSwingDataClass(unittest.TestCase):
    """Test SwingData class"""

    def setUp(self):
        self.swing_data = SwingData("test_swing_data.json")

    def test_get_hit_proportion(self):
        """Test SwingData.get_hit_proportion"""
        hit_proportion = self.swing_data.get_hit_proportion("CU", "1")
        self.assertEqual(hit_proportion, 0.1, f'For CH1 expected: 0.1 but got {hit_proportion}')

        hit_proportion = self.swing_data.get_hit_proportion("FF", "3")
        self.assertEqual(hit_proportion, 0, f'For FF3 expected: 0 but got {hit_proportion}')

    def test_get_out_proportion(self):
        """Test SwingData.get_out_proportion"""
        hit_proportion = self.swing_data.get_out_proportion("CU", "1")
        self.assertEqual(hit_proportion, 0.3, f'For CH1 expected: 0.3 but got {hit_proportion}')

        hit_proportion = self.swing_data.get_out_proportion("FF", "3")
        self.assertEqual(hit_proportion, 0, f'For FF3 expected: 0 but got {hit_proportion}')

    def test_get_strike_proportion(self):
        """Test SwingData.get_strike_proportion"""
        hit_proportion = self.swing_data.get_strike_proportion("CU", "1")
        self.assertEqual(hit_proportion, 0.2, f'For CH1 expected: 0.2 but got {hit_proportion}')

        hit_proportion = self.swing_data.get_strike_proportion("FF", "3")
        self.assertEqual(hit_proportion, 0, f'For FF3 expected: 0 but got {hit_proportion}')
    
    def test_get_foul_proportion(self):
        """Test SwingData.get_foul_proportion"""
        hit_proportion = self.swing_data.get_foul_proportion("CU", "1")
        self.assertEqual(hit_proportion, 0.4, f'For CH1 expected: 0.4 but got {hit_proportion}')

        hit_proportion = self.swing_data.get_strike_proportion("FF", "3")
        self.assertEqual(hit_proportion, 0, f'For FF3 expected: 0 but got {hit_proportion}')
                

if __name__ == '__main__':
    unittest.main()

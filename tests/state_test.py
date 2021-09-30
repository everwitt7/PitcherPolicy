"""State Test Module"""

import unittest

from pitchprediction.state_action_enums import Outcomes
from pitchprediction.state import Count


class TestCountClass(unittest.TestCase):
    """Test Count"""

    def setUp(self):
        self.full = Count(Outcomes, 3, 2)
        self.n_two = Count(Outcomes, 1, 2)
        self.three_n = Count(Outcomes, 3, 1)
        self.n_n = Count(Outcomes, 0, 1)

    def test_get_successor(self):
        """Test Count.get_successor"""

        # test OUT and HIT
        self.assertEqual(self.full.get_successor(
            self.full.outcomes.OUT.value), "out")
        self.assertEqual(self.full.get_successor(
            self.full.outcomes.HIT.value), "hit")

        # test 3-2 count, STRIKE->OUT, BALL->HIT, FOUL->3-2
        self.assertEqual(self.full.get_successor(
            self.full.outcomes.STRIKE.value), "out")
        self.assertEqual(self.full.get_successor(
            self.full.outcomes.BALL.value), "hit")
        self.assertEqual(self.full.get_successor(
            self.full.outcomes.FOUL.value), "32")

        # test 1-2 count, STRIKE->OUT, FOUL->2-2
        self.assertEqual(self.n_two.get_successor(
            self.n_two.outcomes.STRIKE.value), "out")
        self.assertEqual(self.n_two.get_successor(
            self.n_two.outcomes.BALL.value), "22")
        self.assertEqual(self.n_two.get_successor(
            self.n_two.outcomes.FOUL.value), "12")

        # test 3-1 count, BALL-HIT
        self.assertEqual(self.three_n.get_successor(
            self.three_n.outcomes.STRIKE.value), "32")
        self.assertEqual(self.three_n.get_successor(
            self.three_n.outcomes.BALL.value), "hit")
        self.assertEqual(self.three_n.get_successor(
            self.three_n.outcomes.FOUL.value), "32")

        # test 0-1 count
        self.assertEqual(self.n_n.get_successor(
            self.n_n.outcomes.STRIKE.value), "02")
        self.assertEqual(self.n_n.get_successor(
            self.n_n.outcomes.BALL.value), "11")
        self.assertEqual(self.n_n.get_successor(
            self.n_n.outcomes.FOUL.value), "02")

    def test_get_state(self):
        """Test Count.get_state"""
        self.assertEqual(Count.get_state(1, 2), "12")


if __name__ == '__main__':
    unittest.main()

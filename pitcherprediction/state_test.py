"""State Test Module"""


import unittest


from state import CountState


class TestCountStateClass(unittest.TestCase):
    """Test CountState"""

    def setUp(self):
        self.count_state = CountState(0,0)
    
    def test_get_successors(self):
        """Test CountState.get_successors"""
        intended_successors = [CountState(1,0), CountState(0,1)]
        actual_successors = self.count_state.get_successors()

        

        self.assertTrue(itended_successors == actual_successors)
   



if __name__ == '__main__':
    test_classes_to_run = [TestCountStateClass]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
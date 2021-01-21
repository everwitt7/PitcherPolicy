"""Error Distribution Test Module"""

import unittest

from error_dist import NormalErrorDistribution


class TestNormalErrorDistributionClass(unittest.TestCase):
    """Test NormalErrorDistribution class"""

    def setUp(self):
        self.norm_err_dist = NormalErrorDistribution(1, 1)

    def test_gen_actual_loc(self):
        """Test NormalErrorDistribution.gen_actual_loc"""
        x_intended, y_intended = 2, -3
        x_actual, y_actual = self.norm_err_dist.gen_actual_loc(
            x_intended, y_intended)

        x_offset = 4*self.norm_err_dist.sigma_x + self.norm_err_dist.mu_x
        y_offset = 4*self.norm_err_dist.sigma_y + self.norm_err_dist.mu_y

        self.assertTrue(x_intended-x_offset < x_actual < x_intended+x_offset)
        self.assertTrue(y_intended-y_offset < y_actual < y_intended+y_offset)


if __name__ == '__main__':
    test_classes_to_run = [TestNormalErrorDistributionClass]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

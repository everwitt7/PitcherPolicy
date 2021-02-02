"""Run All Tests Module"""

import unittest
from error_dist_test import TestNormalErrorDistributionClass
from zone_test import TestZoneClass
from obvious_zones_test import TestObviousZonesClass
from zones_test import TestZonesClass

if __name__ == '__main__':
    test_classes_to_run = [TestNormalErrorDistributionClass,
                           TestZoneClass, TestObviousZonesClass, TestZonesClass]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

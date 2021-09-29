"""Run All Tests Module"""

import unittest

from pitches.error_dist_test import TestNormalErrorDistributionClass
from pitches.zone_test import TestZoneClass
from pitches.obvious_zones_test import TestObviousZonesClass
from pitches.zones_test import TestZonesClass
from pitches.pitch_test import TestPitchClass
from state_test import TestCountClass

if __name__ == '__main__':
    test_classes_to_run = [TestNormalErrorDistributionClass,
                           TestZoneClass, TestObviousZonesClass,
                           TestZonesClass, TestPitchClass, TestCountClass]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

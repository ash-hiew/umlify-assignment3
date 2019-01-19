from unittests.unittest_shelf import ShelfUnitTests
from unittests.unittest_database import DatabaseUnitTests
from unittests.extractor_unittest import ExtractorUnitTests
from unittests.ucv_unittest import UCVTests
from unittests.cmdline_unittest import InterpreterTests

import unittest


def unit_tests():
    the_suite = unittest.TestSuite()

    the_suite.addTest(unittest.makeSuite(ShelfUnitTests))
    the_suite.addTest(unittest.makeSuite(DatabaseUnitTests))
    the_suite.addTest(unittest.makeSuite(ExtractorUnitTests))
    the_suite.addTest(unittest.makeSuite(UCVTests))
    the_suite.addTest(unittest.makeSuite(InterpreterTests))

    return the_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)

    test_suite = unit_tests()
    runner.run(test_suite)

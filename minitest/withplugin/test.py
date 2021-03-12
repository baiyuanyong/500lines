#!/usr/bin/python
# -*- coding: utf-8 -*-
import minitest
import sys


class TestDemo(minitest.TestCase):
    """Test mathfuc.py"""

    # @classmethod
    # def setUpClass(cls):
    #     print ("this setupclass() method only called once.\n")

    # @classmethod
    # def tearDownClass(cls):
    #     print ("this teardownclass() method only called once too.\n")

    def setUp(self):
        # print ("do something before test : prepare environment.")
        pass

    def tearDown(self):
        # print ("do something after test : clean up.")
        pass

    def test_add(self):
        """Test method add(a, b)"""
        assert 1+2 == 3

    def test_minus(self):
        """Test method minus(a, b)"""
        assert 5-3 != 2


if __name__ == '__main__':
    # loader = minitest.TestLoader()
    # testsuite = minitest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    # runner = minitest.TestRunner()
    # result = runner.run(testsuite)
    # minitest.main(sys.argv[1:])
    import minitest
    minitest.main(sys.modules[__name__])

    # import config

    # conf = config.Config()
    # conf.config(sys.argv[1:])

    # # loader = TestLoader()
    # testsuite = minitest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    # runner = minitest.TestRunner()
    # result = runner.run(testsuite)
    # conf.plugins.end()
    # conf.plugins.beforeTest(test=testsuite)
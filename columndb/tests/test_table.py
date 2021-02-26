import unittest
import os
from columndb.table import Table

PATH = './DATA/TABLE'

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir(PATH)
        cls.table = Table(PATH)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        for i in range(111):
            self.table.put('column_1', f'test{i}', f'test{i}')

        for i in range(111):
            self.table.put('column_2', f'test{i}', f'test{i}')
        
        self.assertIsNotNone(self.table.get('column_1', 'test0'))
        self.assertIsNotNone(self.table.get('column_1', 'test50'))
        self.assertIsNotNone(self.table.get('column_1', 'test110'))
        self.assertIsNotNone(self.table.get('column_2', 'test0'))
        self.assertIsNotNone(self.table.get('column_2', 'test50'))
        self.assertIsNotNone(self.table.get('column_2', 'test110'))

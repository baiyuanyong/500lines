import unittest
import os
from columndb.column import Column

PATH = './DATA/COLUMN'

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir(PATH)
        cls.column = Column('test', PATH)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        for i in range(9):
            self.column.add(f'test{i}', f'test{i}')
        
        self.assertIsNotNone(self.column.get('test0'))
        self.assertIsNone(self.column.get('testing'))
        self.assertFalse(os.path.exists(self.column.path + '/small_0.data'))
        self.assertFalse(os.path.exists(self.column.path + '/small_0.idx'))
        self.assertFalse(os.path.exists(self.column.path + '/big_0.data'))
        self.assertFalse(os.path.exists(self.column.path + '/big_0.idx'))

        for i in range(9, 99):
            self.column.add(f'test{i}', f'test{i}')

        self.assertTrue(os.path.exists(self.column.path + '/small_8.data'))
        self.assertTrue(os.path.exists(self.column.path + '/small_8.idx'))
        self.assertFalse(os.path.exists(self.column.path + '/big_0.data'))
        self.assertFalse(os.path.exists(self.column.path + '/big_0.idx'))
        
        self.assertIsNotNone(self.column.get('test20'))
        self.assertIsNotNone(self.column.get('test80'))

        for i in range(99, 125):
            self.column.add(f'test{i}', f'test{i}')

        self.assertFalse(os.path.exists(self.column.path + '/small_0.data'))
        self.assertFalse(os.path.exists(self.column.path + '/small_0.idx'))
        self.assertFalse(os.path.exists(self.column.path + '/small_9.data'))
        self.assertFalse(os.path.exists(self.column.path + '/small_9.idx'))
        self.assertTrue(os.path.exists(self.column.path + '/big_0.data'))
        self.assertTrue(os.path.exists(self.column.path + '/big_0.idx'))

        self.assertTrue(os.path.exists(self.column.path + '/small_10.data'))
        self.assertTrue(os.path.exists(self.column.path + '/small_11.idx'))
        self.assertEqual(self.column.mt.size, 5)

        self.assertIsNotNone(self.column.get('test20'))
        self.assertIsNotNone(self.column.get('test80'))
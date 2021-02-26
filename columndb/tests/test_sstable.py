import unittest
import os
from columndb.sstable import SSTable

PATH = './DATA/SSTABLE'

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir(PATH)
        mem_dict = {}
        for i in range(10):
            mem_dict[f'test{i}'] = f'test{i}'

        cls.sstable = SSTable(mem_dict, f'{PATH}/test')

    @classmethod
    def tearDownClass(cls):
        # os.rmdir(PATH)
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        self.assertEqual(self.sstable.get('test0'), 'test0')
        self.assertIsNone(self.sstable.get('testing'))

        self.assertEqual(len(self.sstable.to_list()), 10)

        self.assertTrue(os.path.exists(self.sstable.file_name + '.data'))
        self.assertTrue(os.path.exists(self.sstable.file_name + '.idx'))

        self.sstable.remove()
        self.assertFalse(os.path.exists(self.sstable.file_name + '.data'))
        self.assertFalse(os.path.exists(self.sstable.file_name + '.idx'))

import unittest
from columndb.memtable import MEMTable


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memtable = MEMTable()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        for i in range(9):
            result = self.memtable.add(f'test{i}', f'test{i}')
            self.assertFalse(result)
            self.assertEqual(len(self.memtable.table), i+1)

        for i in range(9, 15):
            result = self.memtable.add(f'test{i}', f'test{i}')
            self.assertTrue(result)
            self.assertEqual(len(self.memtable.table), i+1)

        self.assertIsNone(self.memtable.get('testing'))
        self.assertIsNotNone(self.memtable.get('test1'))

        self.memtable.clear()
        self.assertEqual(self.memtable.table, {})
        self.assertEqual(self.memtable.size, 0)

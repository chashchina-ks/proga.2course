import unittest
from bin import gen_bin_tree

class TestGenBinTree(unittest.TestCase):

    def test1(self):
        self.assertEqual(gen_bin_tree(), {'root': 10, 'left': {'root': 31, 'left': {'root': 94, 'left': {'root': 283, 'left': {'root': {}}, 'right': {'root': {}}}, 'right': {'root': 281, 'left': {'root': {}}, 'right': {'root': {}}}}, 'right': {'root': 92, 'left': {'root': 277, 'left': {'root': {}}, 'right': {'root': {}}}, 'right': {'root': 275, 'left': {'root': {}}, 'right': {'root': {}}}}}, 'right': {'root': 29, 'left': {'root': 88, 'left': {'root': 265, 'left': {'root': {}}, 'right': {'root': {}}}, 'right': {'root': 263, 'left': {'root': {}}, 'right': {'root': {}}}}, 'right': {'root': 86, 'left': {'root': 259, 'left': {'root': {}}, 'right': {'root': {}}}, 'right': {'root': 257, 'left': {'root': {}}, 'right': {'root': {}}}}}})

    def test2(self):
        self.assertEqual(gen_bin_tree(2, 3), {'root': 3, 'left': {'root': {}}, 'right': {'root': {}}})

    def test3(self):
        self.assertEqual(gen_bin_tree(3, 5), {'root': 5, 'left': {'root': 16, 'left': {'root': {}}, 'right': {'root': {}}}, 'right': {'root': 14, 'left': {'root': {}}, 'right': {'root': {}}}})

    def test4(self):
        self.assertEqual(gen_bin_tree(1, 7), {'root': {}})

if __name__ == '__main__':
    unittest.main()

import unittest
from bin_2 import gen_bin_tree

class TestGenBinTree(unittest.TestCase):

    def test1(self):
        self.assertEqual(gen_bin_tree(), {10: {'left': 31, 'right': 29}, 31: {'left': 94, 'right': 92}, 29: {'left': 88, 'right': 86}, 94: {'left': 283, 'right': 281}, 92: {'left': 277, 'right': 275}, 88: {'left': 265, 'right': 263}, 86: {'left': 259, 'right': 257}, 283: {'left': 850, 'right': 848}, 281: {'left': 844, 'right': 842}, 277: {'left': 832, 'right': 830}, 275: {'left': 826, 'right': 824}, 265: {'left': 796, 'right': 794}, 263: {'left': 790, 'right': 788}, 259: {'left': 778, 'right': 776}, 257: {'left': 772, 'right': 770}, 850: {'left': None, 'right': None}, 848: {'left': None, 'right': None}, 844: {'left': None, 'right': None}, 842: {'left': None, 'right': None}, 832: {'left': None, 'right': None}, 830: {'left': None, 'right': None}, 826: {'left': None, 'right': None}, 824: {'left': None, 'right': None}, 796: {'left': None, 'right': None}, 794: {'left': None, 'right': None}, 790: {'left': None, 'right': None}, 788: {'left': None, 'right': None}, 778: {'left': None, 'right': None}, 776: {'left': None, 'right': None}, 772: {'left': None, 'right': None}, 770: {'left': None, 'right': None}})

    def test2(self):
        self.assertEqual(gen_bin_tree(2, 3), {3: {'left': 10, 'right': 8}, 10: {'left': None, 'right': None}, 8: {'left': None, 'right': None}})

    def test3(self):
        self.assertEqual(gen_bin_tree(3, 5), {5: {'left': 16, 'right': 14}, 16: {'left': 49, 'right': 47}, 14: {'left': 43, 'right': 41}, 49: {'left': None, 'right': None}, 47: {'left': None, 'right': None}, 43: {'left': None, 'right': None}, 41: {'left': None, 'right': None}})

    def test4(self):
        self.assertEqual(gen_bin_tree(1, 7), {'root': {}})

if __name__ == '__main__':
    unittest.main()

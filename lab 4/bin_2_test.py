"""
Модуль с unit-тестами для нерекурсивной функции gen_bin_tree.

Проверяет корректность генерации бинарного дерева при различных
входных параметрах, включая граничные случаи и пользовательские lambda-функции.
"""

import unittest
from bin_2 import gen_bin_tree


class TestGenBinTree(unittest.TestCase):
    """
    Набор тестов для проверки нерекурсивной функции gen_bin_tree.
    """

    def test_height_zero(self):
        """
        Проверяет, что при height = 0 дерево содержит только корень.
        """
        expected = {10: {'left': None, 'right': None}}
        self.assertEqual(gen_bin_tree(height=0, root=10), expected)

    def test_height_one(self):
        """
        Проверяет, что при height = 1 дерево содержит только корень.
        """
        expected = {10: {'left': None, 'right': None}}
        self.assertEqual(gen_bin_tree(height=1, root=10), expected)

    def test_height_two_default_func(self):
        """
        Проверяет дерево height=2 с функциями по умолчанию (вариант №10).
        """
        expected = {
            10: {'left': 31, 'right': 29},
            31: {'left': None, 'right': None},
            29: {'left': None, 'right': None}
        }
        self.assertEqual(gen_bin_tree(height=2, root=10), expected)

    def test_height_three_default_func(self):
        """
        Проверяет дерево height=3 с функциями по умолчанию.
        """
        expected = {
            10: {'left': 31, 'right': 29},
            31: {'left': 94, 'right': 92},
            29: {'left': 88, 'right': 86},
            94: {'left': None, 'right': None},
            92: {'left': None, 'right': None},
            88: {'left': None, 'right': None},
            86: {'left': None, 'right': None}
        }
        self.assertEqual(gen_bin_tree(height=3, root=10), expected)

    def test_full_tree_variant10(self):
        """
        Полная проверка для варианта №10: height=5, root=10.
        Сравнивает результат с заранее составленным словарём.
        """
        expected = {
            10: {'left': 31, 'right': 29},
            31: {'left': 94, 'right': 92},
            29: {'left': 88, 'right': 86},
            94: {'left': 283, 'right': 281},
            92: {'left': 277, 'right': 275},
            88: {'left': 265, 'right': 263},
            86: {'left': 259, 'right': 257},
            283: {'left': 850, 'right': 848},
            281: {'left': 844, 'right': 842},
            277: {'left': 832, 'right': 830},
            275: {'left': 826, 'right': 824},
            265: {'left': 796, 'right': 794},
            263: {'left': 790, 'right': 788},
            259: {'left': 778, 'right': 776},
            257: {'left': 772, 'right': 770},
            850: {'left': None, 'right': None},
            848: {'left': None, 'right': None},
            844: {'left': None, 'right': None},
            842: {'left': None, 'right': None},
            832: {'left': None, 'right': None},
            830: {'left': None, 'right': None},
            826: {'left': None, 'right': None},
            824: {'left': None, 'right': None},
            796: {'left': None, 'right': None},
            794: {'left': None, 'right': None},
            790: {'left': None, 'right': None},
            788: {'left': None, 'right': None},
            778: {'left': None, 'right': None},
            776: {'left': None, 'right': None},
            772: {'left': None, 'right': None},
            770: {'left': None, 'right': None}
        }
        self.assertEqual(gen_bin_tree(height=5, root=10), expected)

    def test_custom_root(self):
        """
        Проверяет работу с пользовательским значением root.
        """
        expected = {
            5: {'left': 16, 'right': 14},
            16: {'left': None, 'right': None},
            14: {'left': None, 'right': None}
        }
        self.assertEqual(gen_bin_tree(height=2, root=5), expected)

    def test_custom_lambda_functions(self):
        """
        Проверяет работу с пользовательскими lambda-функциями.
        """
        left_func = lambda x: x + 1
        right_func = lambda x: x - 1

        expected = {
            10: {'left': 11, 'right': 9},
            11: {'left': None, 'right': None},
            9: {'left': None, 'right': None}
        }
        self.assertEqual(
            gen_bin_tree(height=2, root=10, left_leaf=left_func, right_leaf=right_func),
            expected
        )

    def test_custom_lambda_functions_height_three(self):
        """
        Проверяет дерево height=3 с пользовательскими lambda-функциями.
        """
        left_func = lambda x: x * 2
        right_func = lambda x: x + 5

        expected = {
            3: {'left': 6, 'right': 8},
            6: {'left': 12, 'right': 11},
            8: {'left': 16, 'right': 13},
            12: {'left': None, 'right': None},
            11: {'left': None, 'right': None},
            16: {'left': None, 'right': None},
            13: {'left': None, 'right': None}
        }
        self.assertEqual(
            gen_bin_tree(height=3, root=3, left_leaf=left_func, right_leaf=right_func),
            expected
        )

    def test_negative_height(self):
        """
        Проверяет поведение при отрицательной высоте.
        Дерево высотой <= 0 содержит только корень.
        """
        expected = {10: {'left': None, 'right': None}}
        self.assertEqual(gen_bin_tree(height=-5, root=10), expected)

    def test_large_height_no_errors(self):
        """
        Проверяет, что дерево большой высоты генерируется без ошибок.
        """
        try:
            tree = gen_bin_tree(height=6, root=10)
            self.assertIsInstance(tree, dict)
            self.assertIn(10, tree)
            # Проверяем, что у корня есть левый и правый потомки
            self.assertIsNotNone(tree[10]['left'])
            self.assertIsNotNone(tree[10]['right'])
        except Exception as e:
            self.fail(f"gen_bin_tree вызвал исключение при height=6: {e}")


if __name__ == '__main__':
    unittest.main()

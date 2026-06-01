"""
Модуль с unit-тестами для функции gen_bin_tree.

Проверяет корректность генерации бинарного дерева при различных
входных параметрах, включая граничные случаи и пользовательские функции.
"""

import unittest
from bin import gen_bin_tree  # Импорт из исправленного модуля


class TestGenBinTree(unittest.TestCase):
    """
    Набор тестов для проверки функции gen_bin_tree.
    """

    def test_height_zero(self):
        """
        Проверяет, что при height=0 возвращается пустой словарь.
        """
        result = gen_bin_tree(height=0, root=10)
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_height_negative(self):
        """
        Проверяет, что при height<0 возвращается пустой словарь.
        """
        result = gen_bin_tree(height=-5, root=10)
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_height_one(self):
        """
        Проверяет, что при height=1 возвращается словарь с одним ключом 'value'.
        """
        result1 = gen_bin_tree(height=1, root=5)
        self.assertEqual(result1, {'value': 5})

        result2 = gen_bin_tree(height=1, root=100)
        self.assertEqual(result2, {'value': 100})

    def test_default_values_variant10(self):
        """
        Проверяет значения по умолчанию согласно варианту №10.
        Вариант №10: root=10, height=5, left_leaf = root*3+1, right_leaf = 3*root-1
        """
        # При height=2 без указания root (должен быть root=10 по умолчанию)
        tree = gen_bin_tree(height=2)

        self.assertIn('value', tree)
        self.assertEqual(tree['value'], 10)
        self.assertIn('left', tree)
        self.assertIn('right', tree)

        # Проверка значений для height=2
        # Левый потомок: left_leaf(10) = 10*3+1 = 31
        self.assertEqual(tree['left']['value'], 31)
        # Правый потомок: right_leaf(10) = 3*10-1 = 29
        self.assertEqual(tree['right']['value'], 29)

    def test_height_two_with_default_func(self):
        """
        Проверяет структуру дерева при height=2 с функциями по умолчанию.
        """
        tree = gen_bin_tree(height=2, root=10)

        expected_tree = {
            'value': 10,
            'left': {'value': 31},
            'right': {'value': 29}
        }
        self.assertEqual(tree, expected_tree)

    def test_height_three_structure(self):
        """
        Проверяет полную структуру дерева при height=3.
        """
        tree = gen_bin_tree(height=3, root=10)

        # Проверка корня
        self.assertEqual(tree['value'], 10)

        # Проверка левого поддерева (начинается с 31)
        self.assertEqual(tree['left']['value'], 31)
        self.assertEqual(tree['left']['left']['value'], 31*3 + 1)  # 94
        self.assertEqual(tree['left']['right']['value'], 3*31 - 1)  # 92

        # Проверка правого поддерева (начинается с 29)
        self.assertEqual(tree['right']['value'], 29)
        self.assertEqual(tree['right']['left']['value'], 29*3 + 1)  # 88
        self.assertEqual(tree['right']['right']['value'], 3*29 - 1)  # 86

    def test_custom_functions(self):
        """
        Проверяет работу с пользовательскими функциями для вычисления потомков.
        """
        left_func = lambda x: x + 1
        right_func = lambda x: x - 1

        tree = gen_bin_tree(height=2, root=10, left_leaf=left_func, right_leaf=right_func)

        expected_tree = {
            'value': 10,
            'left': {'value': 11},
            'right': {'value': 9}
        }
        self.assertEqual(tree, expected_tree)

    def test_custom_functions_height_three(self):
        """
        Проверяет дерево height=3 с пользовательскими функциями.
        """
        left_func = lambda x: x * 2
        right_func = lambda x: x + 5

        tree = gen_bin_tree(height=3, root=3, left_leaf=left_func, right_leaf=right_func)

        # Проверка структуры
        self.assertEqual(tree['value'], 3)
        self.assertEqual(tree['left']['value'], 6)
        self.assertEqual(tree['left']['left']['value'], 12)
        self.assertEqual(tree['left']['right']['value'], 11)
        self.assertEqual(tree['right']['value'], 8)
        self.assertEqual(tree['right']['left']['value'], 16)
        self.assertEqual(tree['right']['right']['value'], 13)

    def test_large_height(self):
        """
        Проверяет, что дерево большой высоты генерируется без ошибок.
        """
        try:
            tree = gen_bin_tree(height=6, root=10)
            self.assertIsInstance(tree, dict)
            self.assertIn('value', tree)
            self.assertIn('left', tree)
            self.assertIn('right', tree)
            self.assertIsInstance(tree['left'], dict)
            self.assertIsInstance(tree['right'], dict)
        except RecursionError:
            self.fail("gen_bin_tree вызвал RecursionError при height=6")

    def test_different_root_value(self):
        """
        Проверяет, что значение root влияет на дерево.
        """
        # С корнем 20
        tree1 = gen_bin_tree(height=2, root=20)
        self.assertEqual(tree1['value'], 20)
        self.assertEqual(tree1['left']['value'], 20*3 + 1)  # 61
        self.assertEqual(tree1['right']['value'], 3*20 - 1)  # 59

        # С корнем 5
        tree2 = gen_bin_tree(height=2, root=5)
        self.assertEqual(tree2['value'], 5)
        self.assertEqual(tree2['left']['value'], 5*3 + 1)  # 16
        self.assertEqual(tree2['right']['value'], 3*5 - 1)  # 14

    def test_tree_keys_format(self):
        """
        Проверяет, что дерево использует правильные ключи: 'value', 'left', 'right'.
        """
        tree = gen_bin_tree(height=2, root=10)

        # Проверка ключей корня
        self.assertIn('value', tree)
        self.assertIn('left', tree)
        self.assertIn('right', tree)

        # Проверка ключей поддеревьев
        self.assertIn('value', tree['left'])
        self.assertIn('value', tree['right'])

        # Проверка, что нет устаревших ключей
        self.assertNotIn('root', tree)
        self.assertNotIn('root', tree['left'])

    def test_variant10_complete(self):
        """
        Комплексная проверка для варианта №10.
        root = 10, height = 5, left_leaf = root * 3 + 1, right_leaf = 3 * root - 1
        """
        tree = gen_bin_tree(height=5, root=10)

        # Проверка на соответствие ожидаемой структуре для первых двух уровней
        self.assertEqual(tree['value'], 10)
        self.assertEqual(tree['left']['value'], 31)
        self.assertEqual(tree['right']['value'], 29)

        # Второй уровень левого поддерева
        self.assertEqual(tree['left']['left']['value'], 94)
        self.assertEqual(tree['left']['right']['value'], 92)

        # Второй уровень правого поддерева
        self.assertEqual(tree['right']['left']['value'], 88)
        self.assertEqual(tree['right']['right']['value'], 86)


if __name__ == '__main__':
    unittest.main()

"""
Модуль для генерации бинарного дерева.

Содержит рекурсивную функцию gen_bin_tree для построения бинарного дерева
заданной высоты с вычислением потомков по заданным алгоритмам.
"""

from typing import Dict, Union, Callable, Optional

# Тип для представления узла дерева
TreeNode = Dict[str, Union[int, 'TreeNode']]


def gen_bin_tree(
        height: int = 5,
        root: int = 10,
        left_leaf: Optional[Callable[[int], int]] = None,
        right_leaf: Optional[Callable[[int], int]] = None
) -> Dict[str, Union[int, Dict]]:
    """
    Генерирует бинарное дерево заданной высоты.

    Рекурсивно строит бинарное дерево, где каждый узел содержит значение
    и ссылки на левое и правое поддеревья.

    Parameters
    height : int, optional
        Высота дерева. Должна быть неотрицательной.
        Если height <= 0, возвращается пустой словарь.
        Если height == 1, возвращается узел только с value.
        По умолчанию 5 (согласно варианту №10).
    root : int, optional
        Значение корневого узла. По умолчанию 10 (вариант №10).
    left_leaf : Callable[[int], int], optional
        Функция для вычисления значения левого потомка.
        Принимает значение текущего узла, возвращает значение левого потомка.
        По умолчанию: lambda x: x * 3 + 1 (вариант №10).
    right_leaf : Callable[[int], int], optional
        Функция для вычисления значения правого потомка.
        Принимает значение текущего узла, возвращает значение правого потомка.
        По умолчанию: lambda x: 3 * x - 1 (вариант №10).

    Returns
    dict
        Словарь, представляющий бинарное дерево.
        Формат: {'value': root, 'left': <поддерево>, 'right': <поддерево>}
        Если height <= 0, возвращает пустой словарь {}.
        Если height == 1, возвращает {'value': root}.

    """
    # Установка функций по умолчанию
    if left_leaf is None:
        left_leaf = lambda x: x * 3 + 1
    if right_leaf is None:
        right_leaf = lambda x: 3 * x - 1

    # Базовые случаи
    if height <= 0:
        return {}

    if height == 1:
        return {'value': root}

    # Рекурсивное построение поддеревьев
    left_subtree = gen_bin_tree(
        height=height - 1,
        root=left_leaf(root),
        left_leaf=left_leaf,
        right_leaf=right_leaf
    )

    right_subtree = gen_bin_tree(
        height=height - 1,
        root=right_leaf(root),
        left_leaf=left_leaf,
        right_leaf=right_leaf
    )

    return {
        'value': root,
        'left': left_subtree,
        'right': right_subtree
    }


def print_tree(tree: Dict, level: int = 0) -> None:
    """
    Вспомогательная функция для красивого вывода дерева на экран.

    Parameters
    tree : dict
        Дерево в формате, возвращаемом функцией gen_bin_tree.
    level : int, optional
        Текущий уровень вложенности (для форматирования отступов).
    """
    if not tree:
        print("  " * level + "None")
        return

    indent = "  " * level
    print(f"{indent}value: {tree.get('value', 'None')}")

    if 'left' in tree or 'right' in tree:
        print(f"{indent}left:")
        print_tree(tree.get('left', {}), level + 1)
        print(f"{indent}right:")
        print_tree(tree.get('right', {}), level + 1)

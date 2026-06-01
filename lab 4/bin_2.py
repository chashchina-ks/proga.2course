"""
Модуль для нерекурсивной генерации бинарного дерева.

Содержит функцию gen_bin_tree для построения бинарного дерева заданной высоты
с использованием обхода в ширину и очереди из модуля collections.
"""

from collections import deque
from typing import Dict, Union, Callable, Optional


def gen_bin_tree(
        height: int = 5,
        root: int = 10,
        left_leaf: Optional[Callable[[int], int]] = None,
        right_leaf: Optional[Callable[[int], int]] = None
) -> Dict[int, Dict[str, Union[int, None]]]:
    """
    Генерирует бинарное дерево заданной высоты нерекурсивным способом.

    Использует обход в ширину с помощью очереди из модуля collections.
    Алгоритм строит дерево уровень за уровнем, начиная с корня.

    Parameters
    height : int, optional
        Высота дерева. Должна быть больше 0.
        При height = 0 возвращается словарь с одним корнем.
        При height = 1 возвращается словарь с корнем, у которого left и right = None.
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
        Формат: {
            значение_узла: {'left': значение_левого_потомка, 'right': значение_правого_потомка},
            ...
        }
        Для листьев left и right равны None.
    """
    # Установка функций по умолчанию согласно варианту №10
    if left_leaf is None:
        left_leaf = lambda x: x * 3 + 1
    if right_leaf is None:
        right_leaf = lambda x: 3 * x - 1

    # Словарь для хранения дерева: ключ - значение узла, значение - словарь с left и right
    tree = {}

    # Базовый случай: дерево высотой 0 или 1
    if height <= 0:
        # Дерево высотой 0 содержит только корень
        tree[root] = {'left': None, 'right': None}
        return tree

    if height == 1:
        tree[root] = {'left': None, 'right': None}
        return tree

    # Инициализация корня
    tree[root] = {'left': None, 'right': None}

    # Очередь для обхода дерева в ширину (содержит значения узлов текущего уровня)
    queue = deque([root])

    current_height = 1

    # Построение дерева уровень за уровнем
    while current_height < height:
        # Список для узлов следующего уровня
        next_level_nodes = []

        # Обрабатываем все узлы текущего уровня
        for _ in range(len(queue)):
            node = queue.popleft()

            # Вычисляем значения левого и правого потомков
            left_value = left_leaf(node)
            right_value = right_leaf(node)

            # Обновляем информацию о потомках текущего узла
            tree[node]['left'] = left_value
            tree[node]['right'] = right_value

            # Добавляем потомков в дерево (если их ещё нет)
            if left_value not in tree:
                tree[left_value] = {'left': None, 'right': None}
            if right_value not in tree:
                tree[right_value] = {'left': None, 'right': None}

            # Добавляем потомков в очередь для следующего уровня
            next_level_nodes.append(left_value)
            next_level_nodes.append(right_value)

        # Переходим к следующему уровню
        queue = deque(next_level_nodes)
        current_height += 1

    return tree

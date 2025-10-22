from collections import deque

def gen_bin_tree(height=5, root=10):

    if height == 1:
        return {'root': {}}

    tree = {root: {'left': None, 'right': None}}
    queue = deque([root])  # Очередь для обхода дерева в ширину

    current_height = 1

    while current_height < height:
        next_level_nodes = deque() # Очередь для узлов следующего уровня

        while queue:
            node = queue.popleft()

            left_leaf = node * 3 + 1
            right_leaf = node * 3 - 1

            tree[node]['left'] = left_leaf
            tree[node]['right'] = right_leaf

            tree[left_leaf] = {'left': None, 'right': None}
            tree[right_leaf] = {'left': None, 'right': None}

            next_level_nodes.append(left_leaf) # Добавляем в очередь для следующего уровня
            next_level_nodes.append(right_leaf)

        queue = next_level_nodes # Переходим к следующему уровню
        current_height += 1

    return tree

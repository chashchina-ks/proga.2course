def gen_bin_tree(height=5, root=10):
    if height == 1:
        return {'root': {}}
    else:
        left_leaf = root * 3 + 1
        right_leaf = root * 3 - 1
        left_tree = gen_bin_tree(height=height - 1, root=left_leaf)
        right_tree = gen_bin_tree(height=height - 1, root=right_leaf)
        tree = {
            'root': root,
            'left': left_tree,
            'right': right_tree
        }
        return tree

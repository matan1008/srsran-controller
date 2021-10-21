def items_in_tree(element, length_name, sub_node_name, tree_name=''):
    if not tree_name:
        tree_name = length_name + '_tree'
    length = int(element.get(length_name, 0))
    for i in range(length):
        yield element.get(tree_name).get(f'Item {i}').get(sub_node_name)

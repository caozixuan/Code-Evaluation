from BI.TreeNode import TreeNode


def create_tree(data, min_sup):
    header_table = {}
    for transaction in data:
        for item in transaction:
            header_table[item] = header_table.get(item, 0) + data[transaction]
    header_table = {k: v for k, v in header_table.items() if v >= min_sup}
    if len(header_table) == 0:
        return None, None
    for k in header_table:
        header_table[k] = [header_table[k], None]
    item_tree = TreeNode('NULL', 1, None)
    i = 1
    for transaction, count in data.items():
        print(i)
        i += 1
        item_dict = {}
        for item in transaction:
            if item in header_table.keys():
                item_dict[item] = header_table[item][0]
        if len(item_dict) > 0:
            ordered_items = [k for k, v in sorted(item_dict.items(), key=lambda p: p[1], reverse=True)]
            update_tree(ordered_items, item_tree, header_table, count)
    return item_tree, header_table


def update_tree(items, item_tree, header_table, count):
    if items[0] in item_tree.children:
        item_tree.children[items[0]].increase(count)
    else:
        item_tree.children[items[0]] = TreeNode(items[0], count, item_tree)
        if header_table[items[0]][1] is None:
            header_table[items[0]][1] = item_tree.children[items[0]]
        else:
            update_header(header_table[items[0]][1], item_tree.children[items[0]])
    if len(items) > 1:
        update_tree(items[1:], item_tree.children[items[0]], header_table, count)


def update_header(node, target_node):
    while node.node_link is not None:
        node = node.node_link
    node.node_link = target_node


def ascend_tree(leaf_node, prefix_path):
    while leaf_node.parent is not None:
        prefix_path.append(leaf_node.name)
        leaf_node = leaf_node.parent


def find_path(tree_node):
    cond_pats = {}
    while tree_node is not None:
        prefix_path = []
        ascend_tree(tree_node, prefix_path)
        if len(prefix_path) > 1:
            cond_pats[frozenset(prefix_path[1:])] = tree_node.count
        tree_node = tree_node.node_link
    return cond_pats


def mine_tree(header_table, min_sup, pre_fix, freq_list):
    head_nodes = [v[0] for v in sorted(header_table.items(), key=lambda p: p[1][0])]
    for head_node in head_nodes:
        new_freq_set = pre_fix.copy()
        new_freq_set.add(head_node)
        freq_list.append(new_freq_set)
        cond_patt_bases = find_path(header_table[head_node][1])
        condition_tree, condition_head = create_tree(cond_patt_bases, min_sup)
        if condition_head is not None:
            mine_tree(condition_head, min_sup, new_freq_set, freq_list)
    return freq_list


def fp_growth(data_set, min_sup):
    min_sup = min_sup * len(data_set)
    data_dict = {}
    for transaction in data_set:
        data_dict[transaction] = data_dict.get(transaction, 0) + 1
    print(0)
    fp_tree, header_table = create_tree(data_dict, min_sup)
    frequent_list = mine_tree(header_table, min_sup, set([]), [])
    for f_set in frequent_list:
        if len(f_set) == 1:
            frequent_list.remove(f_set)
    return frequent_list

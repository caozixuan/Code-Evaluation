import csv


def create_instance(url):
    dic_transactions = {}
    with open(url, "r") as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        for line in reader:
            i = i + 1
            dic_transactions[frozenset(line)] = 1
    return dic_transactions


class TreeNode:
    def __init__(self, name, frequency, parent):
        self.name = name
        self.frequency = frequency
        self.next_node = None
        self.parent = parent
        self.dic_children = {}  # Dictionary containing children where key = name and value points to the node

    def increase_frequency(self, increase_by):
        self.frequency += increase_by

    def display_tree(self, indent=1):
        print_name = str(self.name)
        print(' ' * indent, print_name, ' ', self.frequency)
        for child in self.dic_children.values():
            child.display_tree(indent + 1)


class FPGrowth:
    def __init__(self, transactions):
        self.transactions = transactions

    def create_tree(self, min_support):
        head_table = {}       # Head table containing all the head nodes.

        # Count the frequency for each item.
        for record in self.transactions.keys():
            for item in record:
                head_table[item] = head_table.get(item, 0) + self.transactions[record]

        # Eliminate items based on min_support.
        for key in list(head_table.keys()):
            if head_table[key] < min_support:
                del (head_table[key])

        frequent_item_sets = head_table.keys()

        if len(frequent_item_sets) == 0:
            return None, None

        for key in head_table:
            head_table[key] = [head_table[key], None]

        root = TreeNode("NULL SET", 1, None)

        # Generate the FP Tree.
        for trans_set in self.transactions:
            dic_temp = {}
            frequency = self.transactions[trans_set]

            for item in trans_set:
                if item in frequent_item_sets:
                    dic_temp[item] = head_table[item][0]

            if len(dic_temp) > 0:
                # Sort by frequency.
                ordered_items = [v[0] for v in sorted(dic_temp.items(), key=lambda p:(p[1], int(p[0])), reverse=True)]
                # Update FP Tree using sorted records.
                self.update_tree(ordered_items, root, head_table, frequency)
        return root, head_table

    def update_tree(self, ordered_items, tree_node, head_table, frequency):
        if ordered_items[0] in tree_node.dic_children:
            tree_node.dic_children[ordered_items[0]].increase_frequency(frequency)
        else:
            tree_node.dic_children[ordered_items[0]] = TreeNode(ordered_items[0], frequency, tree_node)
            # Check the head table.
            if not head_table[ordered_items[0]][1]:
                head_table[ordered_items[0]][1] = tree_node.dic_children[ordered_items[0]]
            else:
                self.update_head(head_table[ordered_items[0]][1], tree_node.dic_children[ordered_items[0]])

        if len(ordered_items) > 1:
            self.update_tree(ordered_items[1::], tree_node.dic_children[ordered_items[0]], head_table, frequency)

    def update_head(self, node_test, node_target):
        while node_test.next_node:
            node_test = node_test.next_node
        node_test.next_node = node_target

    def ascend_tree(self, leaf_node, prefix_path):
        if leaf_node.parent:
            prefix_path.append(leaf_node.name)
            self.ascend_tree(leaf_node.parent, prefix_path)

    def find_prefix_path(self, basePat, tree_node):
        conditional_paths = {}

        while tree_node:
            prefix_path = []
            self.ascend_tree(tree_node, prefix_path)

            if len(prefix_path) > 1:
                conditional_paths[frozenset(prefix_path[1:])] = tree_node.frequency

            tree_node = tree_node.next_node

        return conditional_paths

    def mine_tree(self, tree_node, head_table, min_support, prefix, frequent_items):
        bigL = [v[0] for v in sorted(head_table.items(), key=lambda p: p[0])]

        for basePath in bigL:
            new_frequent_set = prefix.copy()
            new_frequent_set.add(basePath)
            frequent_items.append(new_frequent_set)

            condPattBases = self.find_prefix_path(basePath, head_table[basePath][1])
            self.transactions = condPattBases
            my_cinditional_tree, my_head = self.create_tree(min_support)

            if my_head:
                self.mine_tree(my_cinditional_tree, my_head, min_support, new_frequent_set, frequent_items)

    def run_fp_growth(self, min_support):
        min_support *= len(self.transactions)
        my_tree, my_head_table = self.create_tree(min_support)
        # my_tree.display_tree()

        frequent_items = []
        self.mine_tree(my_tree, my_head_table, min_support, set([]), frequent_items)
        print("freqItems=", frequent_items)
        print(len(frequent_items))


if __name__ == "__main__":
    data = create_instance("transaction_records.csv")
    fp_growth = FPGrowth(data)
    fp_growth.run_fp_growth(0.3)

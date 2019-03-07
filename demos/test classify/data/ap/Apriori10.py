import csv
import matplotlib.pyplot as plt

class ComputeApriori:
    def __init__(self, url):
        self.url = url
        self.dic_transactions = {}
        self.dic_support = {}

    def read_data(self):
        with open(self.url, "r") as csvfile:
            reader = csv.reader(csvfile)
            i = 0
            for line in reader:
                i = i + 1
                self.dic_transactions[i] = line

    # Create C1 item set from source data.
    def create_C1(self):
        C1 = list()
        for transaction in self.dic_transactions.values():
            for item in transaction:
                if not int(item) in C1:
                    C1.append(int(item))
        C1.sort()
        C1_str = []
        for item in C1:
            C1_str.append([str(item)])

        return C1_str

    # Convert Ck to Lk based on support threshold.
    def Ck_to_Lk(self, Ck, min_support):
        Lk = list()
        Ck_frost = []
        Ck_with_frequency = {}

        for i in range(len(Ck)):
            Ck_frost.append(frozenset(Ck[i]))

        for item_set in Ck_frost:
            Ck_with_frequency[item_set] = 0

        for transaction in self.dic_transactions.values():
            for item_set in Ck_frost:
                if item_set.issubset(transaction):
                    Ck_with_frequency[item_set] += 1

        record_num = len(self.dic_transactions)
        for i in range(len(Ck_with_frequency)):
            support_value = float(Ck_with_frequency[Ck_frost[i]]) / record_num
            if support_value >= min_support:
                Lk.append(Ck[i])
                self.dic_support[Ck_frost[i]] = support_value
        return Lk

    # Join Lk-1 to become Ck.
    def join_Lk_minus_1(self, Lk_minus_1):
        k = len(Lk_minus_1[0]) + 1
        Ck = []

        for i in range(0, len(Lk_minus_1)):
            L1 = list(Lk_minus_1[i])
            for L2 in Lk_minus_1[i + 1:]:
                if self.is_linkable(L1, L2):
                    Lk_item = [item for item in L1[:k - 2]]
                    L2 = list(L2)
                    if int(L1[k - 2]) < int(L2[k - 2]):
                        Lk_item.append(L1[k - 2])
                        Lk_item.append(L2[k - 2])
                    else:
                        Lk_item.append(L2[k - 2])
                        Lk_item.append(L1[k - 2])
                    Ck.append(Lk_item)
        return Ck

    # Judge whether two item sets can join together.
    def is_linkable(self, Lk_1, Lk_2):
        Lk_1 = list(Lk_1)
        Lk_2 = list(Lk_2)
        k = len(Lk_1)
        for i in range(0, k - 1):
            if Lk_1[i] != Lk_2[i]:
                return False
        return True

    # Derive all subsets of k-1 from an item set of k.
    def generate_subsets(self, item_set):
        count = len(item_set)
        subsets = []

        for i in range(count):
            temp_set = []
            for j in range(count):
                if i == j:
                    continue
                temp_set.append(item_set[j])
            subsets.append(temp_set)
        return subsets

    # Delete item sets whose subsets are not all among the frequent item sets from Lk.
    def prune(self, Lk_minus_1, Ck):
        Ck_pruned = []

        for item_set in Ck:
            flag = True   # Means whether teh item set i
            for item in self.generate_subsets(item_set):
                if item not in Lk_minus_1:
                    flag = False
            if flag:
                Ck_pruned.append(item_set)
        return Ck_pruned

    # Generate rules based on frequent item sets.
    def generate_rules(self, Lk, min_confidence):
        rules = []
        subsets = []
        for frequent_item_set in Lk:
            frequent_item_set_frost = frozenset(frequent_item_set)
            for subset in subsets:
                subset_frost = frozenset(subset)
                if subset_frost.issubset(frequent_item_set):
                    difference = []
                    for item in frequent_item_set:
                        if item not in subset_frost:
                            difference.append(item)
                    difference_frost = frozenset(difference)
                    confidence = self.dic_support[frequent_item_set_frost] / self.dic_support[difference_frost]
                    big_rule = (difference, subset, confidence)
                    if confidence >= min_confidence and big_rule not in rules:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        rules.append(big_rule)
            subsets.append(frequent_item_set)
        return rules

    # Entrance
    def compute_apriori(self, min_support, min_confidence):
        self.read_data()

        frequent_item_sets = []
        L1 = self.Ck_to_Lk(self.create_C1(), min_support)
        frequent_item_sets.extend(L1)
        if len(L1) == 0:
            return self.generate_rules(frequent_item_sets, min_confidence)
        L2 = self.Ck_to_Lk(self.join_Lk_minus_1(L1), min_support)
        frequent_item_sets.extend(L2)
        if len(L2) == 0:
            return self.generate_rules(frequent_item_sets, min_confidence)

        # Keep finding frequent item set Lk until it is empty.
        Lk = L2
        while len(Lk) != 0:
            Ck = self.join_Lk_minus_1(Lk)
            Ck_pruned = self.prune(Lk, Ck)
            Lk = self.Ck_to_Lk(Ck_pruned, min_support)
            frequent_item_sets.extend(Lk)

        return frequent_item_sets
        # return self.generate_rules(frequent_item_sets, min_confidence)


if __name__ == "__main__":
    apriori = ComputeApriori("transaction_records.csv")
    result = apriori.compute_apriori(0.3, 0.4)
    print(result)
    print(len(result))
    # # 创建画布1
    # plt.figure(1)
    # i = 0.1
    # x = []
    # y = []
    # while i < 1:
    #     result = apriori.compute_apriori(i, 0.8)
    #     y.append(len(result))
    #     x.append(i)
    #     i += 0.01
    #
    #     print(i)
    #     # if len(result) <= 21 and len(result) >= 19:
    #     #     print(i, len(result), "123123123123123123")

    # plt.plot(x, y)
    # # 输出已绘制图形
    # plt.show()

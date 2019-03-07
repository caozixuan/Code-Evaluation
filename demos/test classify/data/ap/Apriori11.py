import numpy as np


def create_one(data_set, min_sup):
    c1 = {}
    l1 = set()
    n = len(data_set)
    for data in data_set:
        for item in data:
            item_set = frozenset({item})
            if item_set in c1:
                c1[item_set] += 1
            else:
                c1[item_set] = 1
    for transaction, num in c1.items():
        if num >= min_sup * n:
            l1.add(transaction)
    return l1


def is_linkable(s1, s2):
    if len(s1) != len(s2):
        return False
    list1 = list(s1)
    list2 = list(s2)
    list1.sort()
    list2.sort()
    for i in range(0, len(list1) - 1):
        if list1[i] != list2[i]:
            return False
    if list1[-1] >= list2[-1]:
        return False
    return True


def link(lk):
    ck = set()
    for s1 in lk:
        for s2 in lk:
            if is_linkable(s1, s2):
                ck.add(s1 | s2)
    return ck


def pruning(D, min_sup, ck):
    lk = set()
    temp = {}
    min_num = len(D) * min_sup
    for item_set in ck:
        num_list = [1 if item_set.issubset(x) else 0 for x in D]
        temp[item_set] = np.sum(num_list)
    for key, value in temp.items():
        if value >= min_num:
            lk.add(key)
    return lk


def cut_ck(ck, lk):
    s = set()
    for item_set in ck:
        flag = True
        for item in item_set:
            if (item_set - frozenset({item})) not in lk:
                flag = False
                break
        if flag:
            s.add(item_set)
    return s


def apriori(transaction, min_sup):
    lk = create_one(transaction, min_sup)
    pre_lk = set()
    while lk:
        ck = link(lk)
        ck = cut_ck(ck, lk)
        lk = pruning(transaction, min_sup, ck)
        pre_lk = pre_lk | lk
    return pre_lk

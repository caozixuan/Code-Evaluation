import numpy as np
import matplotlib.pyplot as plt


# determine whether 2 sets can be joined
def isJoinable(set1, set2):
    if len(set1) != len(set2) or 0 == len(set1) or set1[-1] >= set2[-1]:
        return False
    for i in range(len(set1)):
        if set1[i] != set2[i]:
            return False


def getRandomData():
    data_quantity = 10000
    item_type = 100

    prob1 = np.random.normal(0.5, 0.1, item_type)
    prob2 = np.random.normal(0.5, 0.1, item_type)
    ''' normal distribution with mean, standard deviation and output quantity
      these data cannot be generated thoroughly by np.random.random() because 
     if the data are not related at all, the analysis will be meaningless, so
    to satisfy a normal distribution is a better way for we to handle with it '''
    data = []
    for _ in range(data_quantity):  # loop 10000 times
        itemset = []
        prob_first = np.random.rand()
        prob_others = np.random.rand(item_type)
        if prob_first > 0.5:  # threshold
            itemset.append(0)
            for i in range(1, item_type):
                if prob_others[i] < prob1[i]:
                    itemset.append(i)
        else:
            for i in range(1, item_type):
                if prob_others[i] < prob2[i]:
                    itemset.append(i)

        data.append(itemset)

    return data


def preprocess(data):
    itemsets = []
    for i in range(len(data)):
        itemset = set(data[i])  # eliminate duplicate elements
        itemsets.append(itemset)
    return itemsets


'''Apriori 1: if a set is frequent set, then its subsets are all frequent set'''
'''Apriori 2: if a set is not frequent set, any of its supersets is not ferquent set'''
'''reference: https://blog.csdn.net/baimafujinji/article/details/53456931 '''


def getSupport(dataset, itemsets, minSupport):
    support = {}
    for data in dataset:
        for itemset in itemsets:
            listItemset = list(itemset)
            listItemset.sort()
            tupleItemset = tuple(listItemset)  # fixed elements
            if itemset.issubset(data):
                support[tupleItemset] = support.get(tupleItemset, 0) + 1  # compute the number of candidate sets
    return {itemset: count for itemset, count in support.items() if count >= minSupport}


def getAllSubsets(itemset):
    if 0 == len(itemset):
        return []
    result = []
    newSet = []
    for item in itemset:
        for oldSet in result:
            newSet = [oldSet + [item]]
        result.extend(newSet)  # add newSet
    result = result[1:-1]  # remove empty subsets and itemset itself
    for i in range(len(result)):
        result[i].sort()
    return result


'''reference: https://www.cnblogs.com/bigmonkey/p/7405555.html'''


def getAssociaionRules(frequent_itemset, support, minConfidenceRatio):
    rules = []
    for itemset in frequent_itemset:
        subsets = getAllSubsets(itemset)
        for subset in subsets:
            confidence = support[tuple(itemset)] / support[tuple(subset)]
            if confidence >= minConfidenceRatio:
                diffset = set(itemset).difference(set(subset))
                rules.append((tuple(subset), tuple(diffset)))
    return rules


def apriori(dataset, minSupportRatio, minConfidenceRatio):
    dataset = preprocess(dataset)
    frequent_itemset = []
    support = {}
    itemsets = set()
    for data in dataset:
        itemsets |= data  # logic or
    itemsets = [set([itemset, ]) for itemset in itemsets]
    minSupport = int(minSupportRatio * len(dataset))
    while True:
        List = getSupport(dataset, itemsets, minSupport)
        support.update(List)  # add List into support
        if 0 == len(List.items()):
            break
        frequent_itemset.extend(List.keys())
        itemsets = []
        for set1 in List.keys():
            for set2 in List.keys():
                if isJoinable(set1, set2):
                    itemsets.append(set(set1) | set(set2))

    rules = getAssociaionRules(frequent_itemset, support, minConfidenceRatio)
    return frequent_itemset, rules


def print_frequent_itemset(result):
    result.sort()
    print('Frequent Itemset:')
    for s in result:
        result_str = ''
        for item in s:
            result_str += str(item) + ' '
        print(result_str)


if __name__ == '__main__':
    dataset = getRandomData()
    frequent_itemset, rules = apriori(dataset, 0.55, 0.45)
    print_frequent_itemset(frequent_itemset)
    print('Amount of frequent itemsets:')
    print(len(frequent_itemset))

from Data import getRandomData
from Data import preprocess
import numpy as np

def isJoinable(s1, s2):
    if len(s1) != len(s2):
        return False
    if len(s1) == 0:
        return False
    for i in range(len(s1)-1):
        if s1[i] != s2[i]:
            return False
    if s1[-1] >= s2[-1]:
        return False
    return True

def getSupport(Data, itemsets, minSupport):
    support = {}
    for ele in Data:
        for itemset in itemsets:
            listItemset = list(itemset)
            listItemset.sort()
            tupleItemset = tuple(listItemset) 
            if itemset.issubset(ele):
                support[tupleItemset] = support.get(tupleItemset,0) + 1
    return {itemset:count for itemset,count in support.items() if count >= minSupport}
    
def Apriori(Data, minSupportRatio, minConfidenceRatio):
    Data = preprocess(Data)
    frequent_itemset = []
    support = {}
    itemsets = set()
    for ele in Data:
        itemsets |= ele 
    itemsets = [set([itemset,]) for itemset in itemsets]
    minSupport = int(minSupportRatio * len(Data))
    while True:
        L = getSupport(Data, itemsets, minSupport)
        support.update(L)
        if len(L.items()) == 0: 
            break
        frequent_itemset.extend(L.keys())
        itemsets = []
        for set1 in L.keys():
            for set2 in L.keys():
                if isJoinable(set1, set2):
                    itemsets.append(set(set1) | set(set2))
    
    rules = getAssociaionRules(frequent_itemset, support, minConfidenceRatio)
    return frequent_itemset, rules

if __name__ == '__main__':
    Data = getSimpleTestData()
    np.random.seed(0)
    Data = getRandomData()
    frequent_itemset, rules = apriori(Data,0.6,0.6)
    
    print_frequent_itemset(frequent_itemset)
    print_rules(rules)
    print(len(frequent_itemset))
    print(len(rules))
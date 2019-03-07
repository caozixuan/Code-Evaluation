import numpy as np

def getSupport(dataset, itemsets, minSupport):
    support = {}
    for data in dataset:
        for itemset in itemsets:
            tupleItemset = tuple(itemset)
            if itemset.issubset(data):
                support[tupleItemset] = support.get(tupleItemset,0) + 1
    return {itemset:count for itemset,count in support.items() if count >= minSupport}

def printResult(result):
    for s in result:
        setstr = ''
        for item in s:
            setstr += str(item) + ' '
        print(setstr)

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


def apriori(dataset, minSupportRatio):
    itemsets = set()
    result = []
    for data in dataset:
        itemsets |= data
    itemsets = [set([itemset,]) for itemset in itemsets]
    minSupport = int(minSupportRatio * len(dataset))
    while True:
        L = getSupport(dataset, itemsets, minSupport)
        if len(L.items()) == 0:
            break
        result.extend(L)
        itemsets = []
        for set1 in L.keys():
            for set2 in L.keys():
                if isJoinable(set1, set2):
                    itemsets.append(set(set1) | set(set2))
    return result


def getSimpleTestData():
    data = [[0,2,3],
            [2,3,4],
            [0,1,4,5],
            [1,2,3,4],
            [2,4,5]]
    itemsets = []
    for i in range(len(data)):
        itemset = set(data[i])
        itemsets.append(itemset)
    return itemsets

def getRandomData():
    data_no = 10000
    total_product_no = 100
    threshold = 0.56

    possibility1 = np.random.normal(0.47,0.2,total_product_no)
    possibility2 = np.random.normal(0.47,0.2,total_product_no)
    data = []
    for _ in range(data_no):
        itemset = []
        for m in range(0,5):
            possibility_first = np.random.rand()
            possibility_other = np.random.rand(total_product_no)
            if possibility_first > threshold:
                itemset.append(20*m)
                for j in range(20*m+1, 20*(m+1)):
                    if possibility_other[j] < possibility1[j]:
                        itemset.append(j)
            else:
                for j in range(20*m+1, 20*(m+1)):
                    if possibility_other[j] < possibility2[j]:
                        itemset.append(j)
        data.append(itemset)
    itemsets = []
    for i in range(len(data)):
        itemset = set(data[i])
        itemsets.append(itemset)
    return itemsets

if __name__ =='__main__':
    data = getSimpleTestData()
    result = apriori(data,0.4)
    printResult(result)
    print("=====waiting for random part========")
    data=getRandomData()
    result = apriori(data,0.4)
    printResult(result)


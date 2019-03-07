from Data import generateData
from Data import preprocess
from Apriori import apriori
from FPnode import Fpnode

import numpy as np
def compute_frequency(Data):
    frequency = {}
    for ele in Data:
        for item in ele[0]:
            frequency[item] = frequency.get(item,0) + ele[1]
    return frequency

def sort_data(Data, frequency):
    result = []
    for i in range(len(Data)):
        data = Data[i]
        data[0].sort(key=lambda item : frequency[item], reverse=True)
        result.append(data)
    return result

def prune(Data, frequency, minSupport):
    result = []
    for i in range(len(Data)):
        data = Data[i]
        listdata = [item for item in data[0] if frequency[item] >= minSupport]
        result.append((listdata,data[1]))
    return result

def insert_data(data, root, header):
    for item in data[0]:
        if item not in root.child.keys():
            newnode = Fpnode(item)
            newnode.pa = root
            root.child[item] = newnode
            if item not in header.keys():
                header[item] = None
            header[item] = (newnode, header[item])
        root = root.child[item]
        root.count = root.count + data[1]
        
def printFPTree(root):
    print('%s %d' % (root.item, root.count))
    for subnode in root.child.values():
        printFPTree(subnode)
        
def build_fptree(Data, minSupport, suffix):
    if len(Data) == 0:
        return [],{}

    root = Fpnode()
    header = {}
    frequent_itemset = []
    support = {}
    frequency = compute_frequency(Data)
    Data = prune(Data, frequency, minSupport)
    Data = sort_data(Data, frequency)
    for data in Data:
        insert_data(data, root, header)
    
    for h in header.keys():
        sup_count = 0
        t = header[h]
        while t is not None:
            sup_count += t[0].count
            t = t[1]
        listitem = [h] + suffix
        frequent_itemset.append(listitem)
        listitem.sort()
        support[tuple(listitem)] = sup_count
   
    for item in sorted(header.items(), key=lambda item : frequency[item[0]]):
        t = item[1]
        newdataset = []
        while t is not None:
            count = t[0].count
            newdata = []
            panode = t[0].pa
            while not panode.is_root():
                newdata.append(panode.item)
                panode = panode.pa
            newdata.reverse()
            newdata = (newdata, count)
            t = t[1]
            if len(newdata[0]) != 0:
                newdataset.append(newdata)
        newsuffix = [item[0]] + suffix
        new_itemset, new_support = build_fptree(newdataset, minSupport, newsuffix)
        frequent_itemset.extend(new_itemset)
        support.update(new_support)
    
    return frequent_itemset,support

def fpgrowth(Data, minSupportRatio, minConfidenceRatio):
    Data = preprocess(Data)
    Data = [(list(data),1) for data in Data]
    minSupport = int(minSupportRatio * len(Data))
    frequent_itemset, support = build_fptree(Data, minSupport, [])
    rules = getAssociaionRules(frequent_itemset, support, minConfidenceRatio)
    return frequent_itemset,rules

if __name__ == '__main__':
    np.random.seed(0)
    Data = generateData()

    frequent_itemset, rules = fpgrowth(Data,0.6,0.6)
    print_frequent_itemset(frequent_itemset)
    print_rules(rules)
    print(len(frequent_itemset))
    print(len(rules))
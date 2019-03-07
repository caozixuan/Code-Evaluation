import numpy as np
import matplotlib.pyplot as plt

class Fpnode:
    def __init__(self, item='root'):
        self.item = item
        self.parent = None
        self.child = {}
        self.count = 0

    def is_root(self):
        return self.parent is None

def generateData():
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


def printFPTree(root):
    print('%s %d' % (root.item, root.count))
    for subnode in root.child.values():
        printFPTree(subnode)

def compute_frequency(dataset):
    frequency = {}
    for data in dataset:
        for item in data[0]:
            frequency[item] = frequency.get(item,0) + data[1]
    return frequency

def sort_data(dataset, frequency):
    result = []
    for i in range(len(dataset)):
        data = dataset[i]
        data[0].sort(key=lambda item : frequency[item], reverse=True)
        result.append(data)
    return result

def prune(dataset, frequency, minSupport):
    result = []
    for i in range(len(dataset)):
        data = dataset[i]
        listdata = [item for item in data[0] if frequency[item] >= minSupport]
        result.append((listdata,data[1]))
    return result

def insert_data(data, root, header):
    for item in data[0]:
        if item not in root.child.keys():
            newnode = Fpnode(item)
            newnode.parent = root
            root.child[item] = newnode
            if item not in header.keys():
                header[item] = None
            header[item] = (newnode, header[item])
        root = root.child[item]
        root.count = root.count + data[1]

def build_fptree(dataset, minSupport, suffix):
    if len(dataset) == 0:
        return [], {}

    root = Fpnode()
    header = {}
    frequent_itemset = []
    support = {}
    frequency = compute_frequency(dataset)
    dataset = prune(dataset, frequency, minSupport)
    dataset = sort_data(dataset, frequency)
    for data in dataset:
        insert_data(data, root, header)
        # print(data)

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

    for item in sorted(header.items(), key=lambda item: frequency[item[0]]):
        t = item[1]
        newdataset = []
        while t is not None:
            count = t[0].count
            newdata = []
            panode = t[0].parent
            while not panode.is_root():
                newdata.append(panode.item)
                panode = panode.parent
            newdata.reverse()
            newdata = (newdata, count)
            t = t[1]
            if len(newdata[0]) != 0:
                newdataset.append(newdata)
        newsuffix = [item[0]] + suffix
        new_itemset, new_support = build_fptree(newdataset, minSupport, newsuffix)
        frequent_itemset.extend(new_itemset)
        support.update(new_support)

    return frequent_itemset, support

def getAllSubsets(itemset):
    if len(itemset) == 0:
        return []
    result = [[]]
    for item in itemset:
        newSet = [ oldSet + [item] for oldSet in result]
        result.extend(newSet)
    result = result[1:-1]
    for i in range(len(result)):
        result[i].sort()
    return result

def getAssociaionRules(frequent_itemset, support, minConfidenceRatio):
    rules = []
    for itemset in frequent_itemset:
        subsets = getAllSubsets(itemset)
        for subset in subsets:
            confidence = support[tuple(itemset)] / support[tuple(subset)]
            if confidence >= minConfidenceRatio:
                diffset = set(itemset).difference(set(subset))
                rules.append((tuple(subset),tuple(diffset)))
    return rules



def fpgrowth(dataset, minSupportRatio, minConfidenceRatio):
    dataset = [(list(data),1) for data in dataset]
    minSupport = int(minSupportRatio * len(dataset))
    frequent_itemset, support = build_fptree(dataset, minSupport, [])
    rules = getAssociaionRules(frequent_itemset, support, minConfidenceRatio)
    return frequent_itemset,rules

if __name__ == '__main__':

    np.random.seed(0)
    dataset = generateData()

    x = np.linspace(0.30,0.50,20)
    y = []
    for support_ratio in x:
        _, rules = fpgrowth(dataset, support_ratio, 0.8)
        y.append(len(rules))
        print('In graph 1, if confidence = 0.8, and support = %.2f, then rules remaining = %i' % (support_ratio, len(rules)))
    print(y)
    plt.plot(x,y)
    plt.title('Confidence = 80%')
    plt.xlabel('Support')
    plt.ylabel('Rules')
    plt.savefig('../assets/61')
    plt.show()

    x = np.linspace(0.5,0.8,30)
    y = []
    for confidence in x:
        _, rules = fpgrowth(dataset, 0.3, confidence)
        y.append(len(rules))
        print('In graph 2, if support = 0.3, and confidence = %.2f, then rules remaining = %i' % (confidence,len(rules)))
    print(y)
    plt.plot(x,y)
    plt.title('Support = 30%')
    plt.xlabel('Confidence')
    plt.ylabel('Rules')
    plt.savefig('../assets/62')
    plt.show()
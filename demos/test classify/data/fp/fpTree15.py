# coding=utf-8
import fpTree
from Apriori import PowerSetsBinary, Rule
import matplotlib.pyplot as plt
import numpy as np


# 定义一个树，保存树的每一个结点
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}  # 用于存放节点的子节点
        self.nodeLink = None  # 用于连接相似的元素项

    # 对count变量增加给定值
    def inc(self, numOccur):
        self.count += numOccur


# 创建fp树
def createTree(dataSet, minSup):
    # 遍历数据集，统计各元素项出现次数，创建头指针表
    headerTable = {}
    for line in dataSet:
        for item in line:
            headerTable[item] = headerTable.get(item, 0) + dataSet[line]
    # 删除头指针表中不满足最小支持度的项
    for i in headerTable.keys():
        if headerTable[i] < minSup:
            del (headerTable[i])
    # 如果没有一个元素项的频率超过最小支持度，则返回空
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # 在头指针表增加一个数据项，用于存放指向相似元素项指针
    for j in headerTable:
        headerTable[j] = [headerTable[j], None]

    retTree = treeNode('Null Set', 1, None)  # 根节点
    # 再次遍历经过筛选的数据集，创建fp树
    for tranSet, count in dataSet.items():
        localD = {}  # 对一个项集，记录其中每个元素项在数据集中的频数
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]  # 排序
            updateTree(orderedItems, retTree, headerTable, count)  # 更新fp树
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    # 判断事务中的第一个元素项是否作为子节点存在，如果存在则更新该元素项的计数
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    # 如果不存在，则创建一个新的子节点添加到树中
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
            # 对剩下的元素项递归调用本函数
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

        # 辅助函数：获取头指针表中该元素项对应的单链表的尾节点，然后将其指向新节点targetNode


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# 寻找前缀路径，对给定元素项生成一个条件模式基
def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# 辅助函数，直接修改prefixPath的值，将当前节点leafNode添加到prefixPath的末尾，然后递归添加其父节点
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

        # 递归查找频繁项集


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        # 生成条件模式基
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # 创建条件fp树
        myConTree, myHead = createTree(condPattBases, minSup)

        if myHead != None:
            mineTree(myConTree, myHead, minSup, newFreqSet, freqItemList)


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


import random

size = 100


def ge_test_data():
    item_array = []
    for i in range(0, 10000):
        items = []
        for j in range(0, size):
            flag = random.random()
            if flag < 0.1:
                items.append(random.randint(0, size - 1))
        item_array.append(items)
    return item_array


def ge_normal_data(data_size):
    item_array = []
    for i in range(0,data_size):
        normal_array = np.random.normal(0.5, 0.17, size).tolist()
        items = []
        for element in normal_array:
            flag = random.random()
            if flag < 0.1:
                item = int(element/0.01)%size
                items.append(item)
        item_array.append(items)
    return item_array


def ge_association_data(data_size):
    item_array = []
    for i in range(0, data_size):
        association_type = random.randint(0,4)
        items = []
        for j in range(association_type*20,(association_type+1)*20):
            flag2 = random.random()
            if flag2<=0.5:
                items.append(j)
        item_array.append(items)
    return item_array




def getRandomData():
    data_no = 1000
    total_product_no = 100
    threshold = 0.50

    possibility1 = np.random.normal(0.45,0.2,total_product_no)
    possibility2 = np.random.normal(0.45,0.2,total_product_no)
    data = []
    for _ in range(data_no):
        itemset = []
        possibility_first = np.random.rand()
        possibility_other = np.random.rand(total_product_no)
        if possibility_first > threshold:
            itemset.append(0)
            for j in range(1,total_product_no):
                if possibility_other[j] < possibility1[j]:
                    itemset.append(j)
        else:
            for j in range(1,total_product_no):
                if possibility_other[j] < possibility2[j]:
                    itemset.append(j)
        data.append(itemset)
    return data


def cal_support(s, data):
    counter = 0.0
    all_count = len(data)
    for item_set in data:
        if s.issubset(item_set):
            counter+=1.0
    return counter/all_count


def generate_rules(freq_list,data):
    rules = []
    for freq_set in freq_list:
        if len(freq_set)==1:
            continue
        sub_sets = PowerSetsBinary(list(freq_set))
        for set_element in sub_sets:
            cause = set(set_element)
            effect = set(freq_set)-cause
            all_support = cal_support(set(freq_set),data)
            cause_support = cal_support(cause,data)
            rules.append(Rule(cause,effect,all_support/cause_support,all_support))
    return rules


def print_rules(rules, support, confidence):
    counter = 0
    for rule in rules:
        #print str(rule.cause) + '->' + str(rule.effect) + '(support:' + str(rule.support) + ' confidence:' + str(
        #    rule.confidence) + ')'
        if rule.support>=support and rule.confidence >=confidence:
        #    print str(rule.cause) + '->' + str(rule.effect) + '(support:' + str(rule.support) + ' confidence:' + str(
        #        rule.confidence) + ')'
            counter+=1
    return counter

if __name__ == "__main__":
    total_data = [[0, 1, 2, 3], [0, 1, 2], [2, 3], [0, 1, 4]]
    # 最小支持度
    minSup = 200
    test_data = ge_association_data(10000)

    # 初始集合格式化
    initSet = fpTree.createInitSet(test_data)

    # 构建FP树
    myFPtree, myHeaderTab = fpTree.createTree(initSet, minSup)

    # 创建空列表，保存频繁项集
    myFreqList = []
    fpTree.mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
    print "频繁项集个数：", len(myFreqList)
    print "频繁项集：", myFreqList
    rules = generate_rules(myFreqList,initSet)
    rule_nums = []
    ratios = np.linspace(0.2, 0.6, 30)
    for ratio in ratios:
        print ratio
        rule_num = print_rules(rules,0.02,ratio)
        rule_nums.append(rule_num)
        print rule_num
    plt.plot(rule_nums)
    plt.show()

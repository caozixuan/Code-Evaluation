import numpy as np
import matplotlib.pylab as plt


def createSingleSet(dataSet):
    singleSet = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in singleSet:
                singleSet.append([item])
    singleSet.sort()
    return list(map(frozenset, singleSet))


def scanDataSet(dataSet, Ck, minSupport):
    ssCnt = {}
    for tid in dataSet:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(dataSet))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
            supportData[key] = support
    return retList, supportData


def calcSupport(D, Ck, min_support):
    dict_sup = {}
    for i in D:
        for j in Ck:
            if j.issubset(i):
                if not j in dict_sup:
                    dict_sup[j] = 1
                else:
                    dict_sup[j] += 1
    sumCount = float(len(D))
    supportData = {}
    relist = []
    for i in dict_sup:
        temp_sup = dict_sup[i] / sumCount
        if temp_sup >= min_support:
            relist.append(i)
            supportData[i] = temp_sup
    return relist, supportData


def aprioriGenerate(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                a = Lk[i] | Lk[j]  # a为frozenset()集合
                a1 = list(a)
                b = []
                for q in range(len(a1)):
                    t = [a1[q]]
                    tt = frozenset(set(a1) - set(t))
                    b.append(tt)
                t = 0
                for w in b:
                    if w in Lk:
                        t += 1
                if t == len(b):
                    retList.append(b[0] | b[1])
    return retList


def apriori(dataSet, minSupport):
    C1 = createSingleSet(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = calcSupport(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGenerate(L[k - 2], k)
        Lk, supK = scanDataSet(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    del L[-1]
    return L, supportData


def getSubset(fromList, toList):
    for i in range(len(fromList)):
        t = [fromList[i]]
        tt = frozenset(set(fromList) - set(t))
        if not tt in toList:
            toList.append(tt)
            tt = list(tt)
            if len(tt) > 1:
                getSubset(tt, toList)


def calcConf(freqSet, H, supportData, ruleList, minConf):
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        lift = supportData[freqSet] / (supportData[conseq] * supportData[freqSet - conseq])

        if conf >= minConf and lift > 1:
            # print(freqSet - conseq, '-->', conseq, '支持度', round(supportData[freqSet - conseq], 2), '置信度：', conf,
            #       'lift值为：', round(lift, 2))
            ruleList.append((freqSet - conseq, conseq, conf))


def ruleGenerate(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = list(freqSet)
            all_subset = []
            getSubset(H1, all_subset)
            calcConf(freqSet, all_subset, supportData, bigRuleList, minConf)
    return bigRuleList


dataSet = np.random.randint(100, size=[100, 10000])
L, supportData = apriori(dataSet, 0.8)
x=np.linspace(0,1,100)
y=[len(ruleGenerate(L, supportData, i)) for i in x]
plt.plot(x, y)
plt.show()

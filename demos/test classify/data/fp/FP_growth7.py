class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name=nameValue
        self.count=numOccur
        self.nodeLink=None
        self.parent=parentNode
        self.children={}
    def inc(self,numOccur):
        self.count+=numOccur
    def disp(self,ind=1):
        print(' '*ind,self.name,' ',self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataset,minSup=1):
    headerTable={}
    for trans in dataset:
        for item in trans:
            headerTable[item]=headerTable.get(item,0)+dataset[trans]
    #删去未达到支持度的集合
    for k in list(headerTable):
        if headerTable[k]<minSup:
            del (headerTable[k])

    freqItemSet=set(headerTable.keys())

    if len(freqItemSet)==0:
        return None,None

    for k in headerTable:
        headerTable[k]=[headerTable[k],None]

    retTree=treeNode('Null set',1,None)

    for transet,count in dataset.items():
        localD={}
        for item in transet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
        return retTree, headerTable  # 返回树和头指针表

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # 首先检查是否存在该节点
        inTree.children[items[0]].inc(count)  # 存在则计数增加
    else:  # 不存在则将新建该节点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)#创建一个新节点
        if headerTable[items[0]][1] == None:  # 若原来不存在该类别，更新头指针列表
            headerTable[items[0]][1] = inTree.children[items[0]]#更新指向
        else:#更新指向
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  #仍有未分配完的树，迭代
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def ascendTree(leafNode, prefixPath):  #递归上溯整棵树
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):  #参数：指针，节点；
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)#寻找当前非空节点的前缀
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count #将条件模式基添加到字典中
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    # 头指针表中的元素项按照频繁度排序,从小到大
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: str(p[1]))]#python3修改
    for basePat in bigL:  #从底层开始
        #加入频繁项列表
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        print ('finalFrequent Item: ',newFreqSet)
        freqItemList.append(newFreqSet)
        #递归调用函数来创建基
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        print ('condPattBases :',basePat, condPattBases)

        #2. 构建条件模式Tree
        myCondTree, myHead = createTree(condPattBases, minSup)
        #将创建的条件基作为新的数据集添加到fp-tree
        print ('head from conditional tree: ', myHead)
        if myHead != None: #3. 递归
            print ('conditional tree for: ',newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def fpGrowth(dataSet, minSup=3):
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                ['z'],
                ['r', 'x', 'n', 'o', 's'],
                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

    return simpDat

def loadData(filename):
    total = []
    with open(filename, 'r') as f:
        lists = f.readlines()
        for list in lists:
            set = []
            for s in list.split("\t"):
                if (s == "" or s == "\n"):
                    continue
                set.append(int(s))
            if (len(set) != 0):
                total.append(set)
    return total




fpGrowth(loadData("data3.txt"))



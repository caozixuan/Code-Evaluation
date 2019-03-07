SUPPORT=0.3
CONFIDENCE=0.8
NUM=1000

class Association:
    reason=[]
    result=[]
    def __init__(self,reason,result):
        self.reason=reason
        self.result=result
    def __str__(self):
        return str(self.reason)+"=>"+str(self.result)


#从文件中获取数据
def get_data(filename):
    total=[]
    with open(filename,'r') as f:
        lists=f.readlines()
        for list in lists:
            set = []
            for s in list.split("\t"):
                if(s=="" or s=="\n"):
                    continue
                set.append(int(s))
            if(len(set)!=0):
                total.append(set)
    return total

#判断itemSet是否在某一条交易中
def isInLine(itemSet,line):
    for item in itemSet:
        if item not in line:
            return False
    return True


#计算itemSet出现的频率
def get_frequenceOfItemSet(dataset,itemSet):
    frequence = 0
    for line in dataset:
        if isInLine(itemSet,line):
            frequence+=1
    return frequence/NUM


#获取频繁单项集
def get_initialSet(dataset):
    result=[]
    for i in range(100):
        frequence=0
        for line in dataset:
            if i in line:
                frequence+=1
        if (frequence/NUM)>=SUPPORT:
            result.append(i)
    return result

def addItemSet(s,itemset):
    for i in itemset:
        s.append(i)

#由频繁单项集获取频繁二项集
def get2ItemSet(dataset,initialSet):
    itemSet=[]
    for i in range(len(initialSet)-1):
        for j in range(i+1,len(initialSet)):
            curset = []
            curset.append(initialSet[i])
            curset.append(initialSet[j])
            if get_frequenceOfItemSet(dataset,curset)>SUPPORT:
                itemSet.append(curset)
    return itemSet


#由频繁k项集获取频繁k+1项集 (k)->(k+1)
def get_frequentItemSet(dataset,kItemSet):
    if len(kItemSet)==0:
        return []
    newSet=[]
    for i in range(len(kItemSet)-1):
        l1=kItemSet[i]
        l1.sort()
        for j in range(i+1,len(kItemSet)):
            l2=kItemSet[j]
            l2.sort()
            s=[]
            addItemSet(s,l1)
            addItemSet(s,l2)
            s=list(set(s))
            s.sort()
            if len(s)==len(kItemSet[0])+1:
                if s not in newSet:
                    if get_frequenceOfItemSet(dataset,s)>=SUPPORT:
                        newSet.append(s)
    return newSet

def get_AllFrequentSet(dataset,initialSet,TwoItemSet):
    result=[]
    #result.append(initialSet)
    curset=TwoItemSet
    result.append(TwoItemSet)
    for i in range(3,len(dataset[0])+1):
        curset=get_frequentItemSet(dataset,curset)
        if len(curset)==0:
            return result
        result.append(curset)
    return result

#获取频繁项集的总数
def getFrequentNum(result):
    number=0
    for i in result:
        number+=len(i)
    return number

#打印结果
def printResult(result):
    for line  in result:
         print(line)

#判断是否为子集
def isSubset(set1,totalSet):
    if len(set1)>=len(totalSet):
        return False
    for i in set1:
        if i not in totalSet:
            return False
    return True

#获取补集
def getComplement(set1,totalSet):
    x=set(totalSet).difference(set(set1))
    return list(x)

#获取频繁项集,用单个list表示
def getFrequentSet(initialSet,frequentSet):
    result=[]
    newInitialSet=[]
    for i in initialSet:
        set=[]
        set.append(i)
        newInitialSet.append(set)
    addItemSet(result,newInitialSet)
    for kitemset in frequentSet:
        addItemSet(result,kitemset)
    return result

#判断list是否有交集
def isIntersect(list1,list2):
    for i in list1:
        for j in list2:
            if i==j:
                return True
    return False

def getAssociation(dataset,frequentSet,confidence):
    result=[]
    for i in range(len(frequentSet)-1):
        set1=frequentSet[i]
        for j in range(i+1,len(frequentSet)):
            set2=frequentSet[j]
            if not isSubset(set1,set2):
                continue
            set1Support=get_frequenceOfItemSet(dataset,set1)
            set2Support=get_frequenceOfItemSet(dataset,set2)
            comSet=getComplement(set1,set2)
            if len(comSet)==0:
                continue
            if set2Support/set1Support>=confidence:
                    result.append(Association(set1,comSet))
                    #print(Association(set1,comSet))
                    # with open("result data/association.txt",'a+') as f:
                    #     f.write(str(Association(set1,comSet))+"\n")

    return result

if __name__=="__main__":
	dataset=get_data("data3.txt")
	initialSet=get_initialSet(dataset)
	twoItemSet=get2ItemSet(dataset,initialSet)
	result=get_AllFrequentSet(dataset,initialSet,twoItemSet)
	finalSet=getFrequentSet(initialSet,result)
	printResult(finalSet)
	associations=getAssociation(dataset,finalSet,CONFIDENCE)
	print("Frequent set number:"+str(getFrequentNum(result)))
	print("Association number:"+str(len(associations)))
	if input("Press q to quit:")=="q":
		print("End")

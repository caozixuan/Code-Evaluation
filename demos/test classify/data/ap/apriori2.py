#  -*-coding: utf-8-*-
#  author: evan choo
#  creation date: 2018-10-18

from numpy import *
import sys

#  change this function so you can import data in different ways
#  argv:
#  return: 
#    data set that contains all transactions
def load_data():
	file=open(r'./retail.dat.txt', 'r')
	totallist=[]
	for i in range(100):
		line=file.readline()
		string_list=line.split(' ')
		length=len(string_list)
		string_list.remove(string_list[length-1])
		int_list=map(string_2_int, string_list)
		totallist.append(int_list)
	file.close()
	return totallist
	#return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def string_2_int(str):
	return int(str)

#  this function is used to generate all items and store them in C1
#  argv:
#    data_set: data set containing all transactions
#  return:
#    a set that contains all items
def create_C1(data_set):
	C1=[]
	for transaction in data_set:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])

	C1.sort()

	return map(frozenset, C1)


#  this function is used to sort out the L1 set
#  argv:
#    data_set
#    Ck: candidate set list
#    min_support
#  return:
#    ret_list: sets that meets the minimum support
#    support_data: how many transactions contain this set
def scan_database(data_set, Ck, min_support):
	#this dictionary is used to store the count corresponding to the set
	count_for_set={}
	for transaction in data_set:
		for candidate in Ck:
			if candidate.issubset(transaction):
				if not candidate in count_for_set:
					count_for_set[candidate]=1
				else:
					count_for_set[candidate]+=1
	#this is the number of transactions in data set
	number_of_transactions=float(len(data_set))
	#use this list to store qualified sets
	ret_list=[]
	support_data={}
	for key in count_for_set:
		support=count_for_set[key]/number_of_transactions
		if support >= min_support:
			ret_list.insert(0, key)
		support_data[key]=support

	return ret_list, support_data


#  this function is intended to generate the next generation of frequent itemset
#  i.e. if now every frequent itemset has n elements, then this function is going to generate
#  frequent itemset that has (n+1) elements
#  argv:
#    Lk: the frequent itemset that has k elements
#    k: how many elements does this generation of frequent itemsets have
#  return:
#    ret_list: the next generation of frequent itemsets
def apriori_generation(Lk, k):
	ret_list=[]
	length_of_Lk=len(Lk)

	for i in range(length_of_Lk):
		for j in range(i+1, length_of_Lk):
			L1=list(Lk[i])[:k-2]
			L2=list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			if L1==L2:
				#Union lki and lkj
				ret_list.append(Lk[i]|Lk[j])

	return ret_list;


#  apriori
def apriori(data_set, min_support=0.5):
	C1=create_C1(data_set)
	D=map(set, data_set)
	L1, support_data=scan_database(D, C1, min_support)
	L=[L1]
	k=2
	while(len(L[k-2])>0):
		Ck=apriori_generation(L[k-2], k)
		Lk, support_k=scan_database(D, Ck, min_support)
		support_data.update(support_k)
		L.append(Lk)
		k+=1
	return L, support_data


#生成关联规则
def generateRules(L, supportData, minConf=0.7):
    #频繁项集列表、包含那些频繁项集支持数据的字典、最小可信度阈值
    bigRuleList = [] #存储所有的关联规则
    for i in range(1, len(L)):  #只获取有两个或者更多集合的项目，从1,即第二个元素开始，L[0]是单个元素的
        # 两个及以上的才可能有关联一说，单个元素的项集不存在关联问题
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            #该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            if (i > 1):
            #如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:#第一层时，后件数为1
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)# 调用函数2
    return bigRuleList

#生成候选规则集合：计算规则的可信度以及找到满足最小可信度要求的规则
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    #针对项集中只有两个元素时，计算可信度
    prunedH = []#返回一个满足最小可信度要求的规则列表
    for conseq in H:#后件，遍历 H中的所有项集并计算它们的可信度值
        conf = supportData[freqSet]/supportData[freqSet-conseq] #可信度计算，结合支持度数据
        if conf >= minConf:
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
            brl.append((freqSet-conseq, conseq, conf))#添加到规则里，brl 是前面通过检查的 bigRuleList
            prunedH.append(conseq)#同样需要放入列表到后面检查
    return prunedH

#合并
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    #参数:一个是频繁项集,另一个是可以出现在规则右部的元素列表 H
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #频繁项集元素数目大于单个集合的元素数
        Hmp1 = apriori_generation(H, m+1)#存在不同顺序、元素相同的集合，合并具有相同部分的集合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)#计算可信度
        if (len(Hmp1) > 1):    
        #满足最小可信度要求的规则列表多于1,则递归来判断是否可以进一步组合这些规则
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


def execute_apriori(min_support, minConf):
	dataset=load_data()
	print "load completed"
	L, supportdata=apriori(dataset, min_support)
	print "find frequent set completed"
	rules=generateRules(L, supportdata, minConf)
	print "rules generation compelted"
	print len(rules)




# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
 
	C1.sort()
	return list(map(frozenset, C1))

def scanD(D,Ck,minSupport):
	ssCnt={}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if not can in ssCnt:
					ssCnt[can]=1
				else: ssCnt[can]+=1
	numItems=float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support >= minSupport:
			retList.insert(0,key)
		supportData[key] = support
	return retList, supportData
 
def aprioriGen(Lk, k):							
	retList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i+1, lenLk):
			L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
			L1.sort(); L2.sort()
			if L1==L2:
				retList.append(Lk[i] | Lk[j])
	return retList
 
def apriori(dataSet, minSupport = 0.5):
	C1 = createC1(dataSet)
	D = list(map(set, dataSet)) 
	L1, supportData = scanD(D, C1, minSupport)
	L = [L1]
	k = 2
	while (len(L[k-2]) > 0):					
		Ck = aprioriGen(L[k-2], k)
		Lk, supK = scanD(D, Ck, minSupport)
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L, supportData

def generateRules(L, supportData, minConf=0.7):
	bigRuleList = []
	for i in range(1, len(L)):	
		for freqSet in L[i]:
			H1 = [frozenset([item]) for item in freqSet]
			rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
	return len(bigRuleList)
 
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
	prunedH = []
	for conseq in H:
		conf = supportData[freqSet]/supportData[freqSet-conseq]
		if conf >= minConf:
			print(freqSet-conseq, '-->', conseq, 'conf:', conf)
			brl.append((freqSet-conseq, conseq, conf))
			prunedH.append(conseq)
	return prunedH
 
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
	m = len(H[0])
	while (len(freqSet) > m):
		H = calcConf(freqSet, H, supportData, brl, minConf)
		if (len(H) > 1):
			H = aprioriGen(H, m + 1)
			m += 1
		else:
			break

def readData(file):
	transactions=[]
	with open(file,'r') as f:
		for line in f.readlines():
			transactions.append(list(map(str,line.strip().split(','))))
	return transactions

def getCount_SupChange():
	suppStep=0.002
	supp=0.3
	conf=0.8
	x=[]
	y=[]
	dataSet = readData("data.txt")
	
	while(supp>=0.25):
		x.append(supp)
		L,suppData = apriori(dataSet,supp)
		print ("\nminConf= %.2f, minSupport= %.3f 时" % (conf,supp))
		rulesCount = generateRules(L,suppData, conf)
		y.append(rulesCount)
		print ("Count: %d" % rulesCount)
		supp-=suppStep
	
	plt.plot(x, y)
	plt.show()

def getCount_CofChange():
	confStep=0.02
	supp=0.3
	conf=0.8
	x=[]
	y=[]
	dataSet = readData("data.txt")
	
	while(conf>=0.45):
		x.append(conf)
		L,suppData = apriori(dataSet,supp)
		print ("\nminConf= %.2f, minSupport= %.3f 时" % (conf,supp))
		rulesCount = generateRules(L,suppData, conf)
		y.append(rulesCount)
		print ("Count: %d" % rulesCount)
		conf-=confStep

	plt.plot(x, y)
	plt.show()

def getSup():
	suppStep=0.0001
	supp=0.2398
	conf=0.8
	x=[]
	y=[]
	dataSet = readData("data.txt")
	
	while(supp>=0.239):
		x.append(supp)
		L,suppData = apriori(dataSet,supp)
		print ("\nminConf= %.2f, minSupport= %.4f :" % (conf,supp))
		rulesCount = generateRules(L,suppData, conf)
		y.append(rulesCount)
		print ("Count: %d" % rulesCount)
		if(rulesCount>=20):
			break
		supp-=suppStep

getCount_CofChange()
getCount_SupChange()
getSup()

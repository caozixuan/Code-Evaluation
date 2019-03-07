# -*- coding: utf-8 -*-

import get_data as g
import datetime

def apriori(data_set, support, confidence):
	C1 = creat_C1(data_set)
	D = list(map(set, data_set))  # conversion to set. 
	L1, item_support = prune(D, C1, support)
	L = [L1]
	k = 2

	while (len(L[k-2]) > 0):
		print "join L%d" %(k-1)  # print log
		Ck = join(L[k-2],k)
		print "prune L%d" %(k-1)  # print log 
		Lk, sup = prune(D, Ck, support)
		L.append(Lk)
		item_support.update(sup)  # add sup's key-value pairs into item_support
		k += 1

	# generate association rules
	rule_list = generate_rule(L, confidence, item_support)
	return L, item_support, rule_list

def apriori_test(data_set, support, conf_list):
	C1 = creat_C1(data_set)
	D = list(map(set, data_set))  # conversion to set. 
	L1, item_support = prune(D, C1, support)
	L = [L1]
	k = 2

	while (len(L[k-2]) > 0):
		print "join L%d" %(k-1)  # print log
		Ck = join(L[k-2],k)
		print "prune L%d" %(k-1)  # print log 
		Lk, sup = prune(D, Ck, support)
		L.append(Lk)
		item_support.update(sup)  # add sup's key-value pairs into item_support
		k += 1

	rule_list_list = []

	for conf in conf_list:
		# generate association rules
		rule_list = generate_rule(L, conf, item_support)
		rule_list_list.append(rule_list)
	return rule_list_list


def creat_C1(data_set):
	"""Create C1, which is the candidate 1-item set. """
	C1 = []
	for transaction in data_set:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])  # add all item into C1 unrepeatly

	C1.sort()
	# conversion to set. fozenset means user can't change it.
	return list(map(frozenset, C1))  

def prune(data_set, Ck, support):
	"""Create Lk from Ck.
	Lk is the k-item set that has removed items that doesn't meet mini support.
	"""
	item_count_dic = {} 
	for transaction in data_set:
		for item in Ck:
			if item.issubset(transaction):
				if not item in item_count_dic:
					item_count_dic[item] = 1
				else: item_count_dic[item] += 1
	# conversion length to float to do division
	data_set_num = float(len(data_set))  
	L = []
	item_support = {}
	for key in item_count_dic:
		sup = item_count_dic[key] / data_set_num
		item_support[key] = sup
		if sup >= support:
			L.append(key)
	return L, item_support

def join(Lk, k):
	Ck = []
	Lk_len = len(Lk)
	for i in range(Lk_len):
		print "First set: the %d set of L%d" %(i,k-1)  # print log
		for j in range(i+1, Lk_len):
			print  "Second set: the %d set of L%d" %(j,k-1)  # print log
			L1 = list(Lk[i])[:k-2]
			L2 = list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			if L1 == L2:  # if previous k-1 items all the same 
				Ck.append(Lk[i]|Lk[j]) # set union
	return Ck 

def generate_rule(L, confidence, item_support):
	rule_list = []
	sub_set_list = []
	for i in range(0, len(L)):
		for freq_set in L[i]:
			calculate_confidence(freq_set, sub_set_list, 
				item_support, confidence, rule_list)
	return rule_list

def  calculate_confidence(freq_set, sub_set_list, 
	item_support, confidence, rule_list):
	for sub_set in sub_set_list:
		if sub_set.issubset(freq_set):
			conf = item_support[freq_set] / item_support[freq_set - sub_set]
			rule = (freq_set - sub_set, sub_set, conf)
			if conf >= confidence and rule not in rule_list:
				# print freq_set-sub_set, " => ", sub_set, "conf: ", conf
				rule_list.append(rule)
	sub_set_list.append(freq_set)
	return rule_list

if __name__== "__main__":
	starttime = datetime.datetime.now()
	print "Apriori algorithm begin"+"="*28
	data_set = g.get_data()
	# data_set = g.getSimpleTestData2()
	support = 0.4
	confidence = 0.5
	L, item_support, rule_list = apriori(data_set, support, confidence)
	for Lk in L:
		if len(Lk) > 0:
			print "="*50
			print "frequent " + str(len(list(Lk[0]))) + "-itemsets\t\tsupport"
			print "="*50
			for freq_set in Lk:
				print freq_set, "\t\t", item_support[freq_set]
	print
	print "Association rules"+"="*33
	for item in rule_list:
		print item[0], "=>", item[1], "confidence: ", item[2]
	print "Apriori algorithm end"+"="*29
	endtime = datetime.datetime.now()
	print "use time: ", (endtime - starttime).seconds

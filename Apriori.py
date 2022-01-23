# -*- coding:utf-8 -*-
import os,json,re
import Levenshtein

path_ingre = os.getcwd() + "/ingredients_new.json"
match_ingre = os.getcwd() + "/match_ingre.json"
path_m = os.getcwd() + "\\MainMaterList3-14.json"


# 原食材名称-辅料
def getsubIngre(item,subIngre):
    a = 0
    sub_materials = []
    try:
        if len(item['配料']):
            for m in item['配料']:
                for material, kg in m.items():
                    sub_materials.append(material)
    except:
        a = a + 1
    try:
        if len(item['辅料']):
            for m in item['辅料']:
                for material, kg in m.items():
                    sub_materials.append(material)
    except:
        a = a + 1
    if len(sub_materials) > 0:
        subIngre.append(sub_materials)
    else:
        print(item['url'], '未添加')
    return subIngre

# 原食材名称-主料
def getmainIngre(item,mainIngre):
    materials = []
    lists= []
    if len(item['主料']) > 1:
        for m in item['主料']:
            for material,kg in m.items():
                materials.append(material)
        mainIngre.append(materials)

# 原食材名称
def getDataSet():
    path = os.getcwd() + "\\data05.json"
    mainIngre = []
    subIngre = []

    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        for key,value in data.items():
            for item in value:
                getsubIngre(item, subIngre)
                getmainIngre(item, mainIngre)
                # sub_materials = []
                #
                # try:
                #     if len(item['配料']):
                #         for m in item['配料']:
                #             for material,kg in m.items():
                #                 sub_materials.append(material)
                # except:
                #     a = a + 1
                # try:
                #     if len(item['辅料']):
                #         for m in item['辅料']:
                #             for material,kg in m.items():
                #                 sub_materials.append(material)
                # except:
                #     a = a + 1
                # if len(sub_materials) > 1:
                #     subIngre.append(sub_materials)
                # else:
                #     print(item['url'],'未添加')


    return mainIngre


# 获取新数据
def getnewdata():
    with open(match_ingre, encoding='utf-8') as m_ingre:
        data_m = json.load(m_ingre)
    return data_m



def loadDataSet():
   return [['a', 'c', 'e'], ['b', 'd'], ['b', 'c'], ['a', 'b', 'c', 'd'], ['a', 'b'], ['b', 'c'], ['a', 'b'],
            ['a', 'b', 'c', 'e'], ['a', 'b', 'c'], ['a', 'c', 'e']]


# 将所有元素转换为frozenset型字典，存放到列表中
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # print('C1',C1)   # C1  [['a'], ['b'], ['c'], ['d'], ['e']]
    # 映射为frozenset唯一性的，可使用其构造字典,使用frozenset是为了后面可以将这些值作为字典的键
    return list(map(frozenset, C1))   # frozenset一种不可变的集合，set可变集合

# 过滤掉不符合支持度的集合  从候选K项集到频繁K项集（支持度计算）
# 返回 频繁项集列表retList 所有元素的支持度字典
def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:  # 遍历数据集
        for can in Ck:  # 遍历候选项
            if can.issubset(tid):  # 判断候选项中是否含数据集的各项
                # 判断can是否是tid的《子集》 （这里使用子集的方式来判断两者的关系）
                if not can in ssCnt:   # 统计该值在整个记录中满足子集的次数（以字典的形式记录，frozenset为键）
                    ssCnt[can] = 1  # 不含设为1
                else:
                    ssCnt[can] += 1  # 有则计数加1
    numItems = float(len(D))  # 数据集大小
    retList = []  # L1初始化 # 重新记录满足条件的数据值（即支持度大于阈值的数据)
    supportData = {}  # 记录候选项中各个数据的支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems  # 计算支持度
        if support >= minSupport:
            retList.insert(0, key)  # 满足条件加入L1中
            supportData[key] = support
    return retList, supportData  # 排除不符合支持度元素后的元素 每个元素支持度


def calSupport(D, Ck, min_support):
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
            # 此处可设置返回全部的支持度数据（或者频繁项集的支持度数据）
            supportData[i] = temp_sup
    # print('relist', relist)    # relist [frozenset({'a'}), frozenset({'c'}), frozenset({'e'}), frozenset({'b'}), frozenset({'d'})]
    # print('supportData', supportData)  # supportData {frozenset({'a'}): 0.7, frozenset({'c'}): 0.7, frozenset({'e'}): 0.3, frozenset({'b'}): 0.8, frozenset({'d'}): 0.2}
    return relist, supportData


# 频繁项集列表Lk 项集元素个数k  [frozenset({2, 3}), frozenset({3, 5})] -> [frozenset({2, 3, 5})]
# 改进剪枝算法
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):  # 两两组合遍历   # 两层循环比较Lk中的每个元素与其它元素
            L1 = list(Lk[i])[:k - 2]  # 将集合转为list后取值
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()  #该函数每次比较两个list的前k-2个元素，如果相同则求并集得到k个元素的集合
            if L1 == L2:  # 前k-1项相等，则可相乘，这样可防止重复项出现
                # 进行剪枝（a1为k项集中的一个元素，b为它的所有k-1项子集）
                a = Lk[i] | Lk[j]  # a为frozenset()集合
                a1 = list(a)
                b = []
                # 遍历取出每一个元素，转换为set，依次从a1中剔除该元素，并加入到b中
                for q in range(len(a1)):
                    t = [a1[q]]
                    tt = frozenset(set(a1) - set(t))
                    b.append(tt)
                t = 0
                for w in b:
                    # 当b（即所有k-1项子集）都是Lk（频繁的）的子集，则保留，否则删除。
                    if w in Lk:
                        t += 1
                if t == len(b):
                    retList.append(b[0] | b[1])
    return retList


def apriori(dataSet, minSupport=0.2):   # 设置阈值
    # print('1',minSupport)

    # 前3条语句是对计算查找单个元素中的频繁项集
    C1 = createC1(dataSet)  # 将每个元素转会为frozenset字典    [frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}), frozenset({5})]
    D = list(map(set, dataSet))  # 使用list()转换为列表  [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]
    L1, supportData = calSupport(D, C1, minSupport)
    L = [L1]  # 加列表框，使得1项集为一个单独元素
    k = 2
    while (len(L[k - 2]) > 0):  # 是否还有候选集
        Ck = aprioriGen(L[k - 2], k)  # Ck候选频繁项集
        Lk, supK = scanD(D, Ck, minSupport)  # scan DB to get Lk   # Lk频繁项集
        supportData.update(supK)  # 把supk的键值对添加到supportData里
        L.append(Lk)  # L最后一个值为空集
        k += 1
    del L[-1]  # 删除最后一个空集

    # print('L',L) # L [[frozenset({'a'}), frozenset({'c'}), frozenset({'e'}), frozenset({'b'}), frozenset({'d'})], [frozenset({'b', 'e'}), frozenset({'d', 'c'}), frozenset({'d', 'a'}), frozenset({'b', 'a'}), frozenset({'b', 'c'}), frozenset({'d', 'b'}), frozenset({'e', 'c'}), frozenset({'e', 'a'}), frozenset({'c', 'a'})], [frozenset({'c', 'b', 'e'}), frozenset({'a', 'b', 'e'}), frozenset({'c', 'b', 'a'}), frozenset({'d', 'b', 'a'}), frozenset({'d', 'b', 'c'}), frozenset({'d', 'a', 'c'}), frozenset({'e', 'a', 'c'})], [frozenset({'a', 'e', 'b', 'c'}), frozenset({'a', 'd', 'b', 'c'})]]
    # print('supportData',supportData) #  supportData {frozenset({'a'}): 0.7, frozenset({'c'}): 0.7, frozenset({'e'}): 0.3, frozenset({'b'}): 0.8, frozenset({'d'}): 0.2, frozenset({'c', 'a'}): 0.5, frozenset({'e', 'a'}): 0.3, frozenset({'e', 'c'}): 0.3, frozenset({'d', 'b'}): 0.2, frozenset({'b', 'c'}): 0.5, frozenset({'b', 'a'}): 0.5, frozenset({'d', 'a'}): 0.1, frozenset({'d', 'c'}): 0.1, frozenset({'b', 'e'}): 0.1, frozenset({'e', 'a', 'c'}): 0.3, frozenset({'d', 'a', 'c'}): 0.1, frozenset({'d', 'b', 'c'}): 0.1, frozenset({'d', 'b', 'a'}): 0.1, frozenset({'c', 'b', 'a'}): 0.3, frozenset({'a', 'b', 'e'}): 0.1, frozenset({'c', 'b', 'e'}): 0.1, frozenset({'a', 'd', 'b', 'c'}): 0.1, frozenset({'a', 'e', 'b', 'c'}): 0.1}


    return L, supportData  # L为频繁项集，为一个列表，1，2，3项集分别为一个元素; supportData为支持度


# 生成集合的所有子集
def getSubset(fromList, toList):
    for i in range(len(fromList)):
        t = [fromList[i]]
        tt = frozenset(set(fromList) - set(t))
        if not tt in toList:
            toList.append(tt)
            tt = list(tt)
            if len(tt) > 1:
                getSubset(tt, toList)


def calcConf(freqSet, H, supportData, ruleList, minConf=0.7):
    # print('2',minConf)

    for conseq in H:  # 遍历H中的所有项集并计算它们的可信度值
        conf = supportData[freqSet] / supportData[freqSet - conseq]  # 可信度计算，结合支持度数据
        # 提升度lift计算lift = p(a & b) / p(a)*p(b)
        lift = supportData[freqSet] / (supportData[conseq] * supportData[freqSet - conseq])
        # print(freqSet - conseq, '-->', conseq, '支持度', round(supportData[freqSet], 6), '置信度：', round(conf, 6),
        #       'lift值为：', round(lift, 6))

        if conf >= minConf and lift > 1:
            print(freqSet - conseq, '-->', conseq, '支持度', round(supportData[freqSet], 6), '置信度：', round(conf, 6),
                  'lift值为：', round(lift, 6))   # round 四舍五入留6位小数
            ruleList.append((freqSet - conseq, conseq, conf))
    f_main = open('apriori_res_1-22.json', 'w', encoding='utf-8')
    f_main.write(str(ruleList))
    f_main.close()
    # print('ruleList',ruleList)


# 生成规则
def gen_rule(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):  # 从二项集开始计算
        for freqSet in L[i]:  # freqSet为所有的k项集
            # 求该三项集的所有非空子集，1项集，2项集，直到k-1项集，用H1表示，为list类型,里面为frozenset类型，
            H1 = list(freqSet)
            all_subset = []
            getSubset(H1, all_subset)  # 生成所有的子集
            calcConf(freqSet, all_subset, supportData, bigRuleList, minConf)
    return bigRuleList

dataset = getnewdata()
# getDataSet()
# print(dataset)
L, supportData = apriori(dataset, minSupport=0.001) # 最小支持度
rule = gen_rule(L, supportData, minConf=0.2) # 最小置信度
#
# 输出支持度，置信度大于最小值的规则
rule
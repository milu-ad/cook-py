# -*- coding:utf-8 -*-
import os,json,re,csv
import difflib
import Levenshtein
import collections,math

cookstyleList, cuisineList, MainMaterList, tasteList = [], [], [], []
cookstyleID, cuisineID, ingredientID, tasteID = [], [], [], []
path_ingre = os.getcwd() + "/ingredients_new.json"
path_submater = os.getcwd() + "/SubMaterList0.json"
path_m = os.getcwd() + "\\MainMaterList3-14.json"
typecount_data = []
citylists = ['chuancai', 'huicai', 'xiangcai', 'lucai', 'mincai', 'sucai', 'yuecai', 'zhecai']
ingrelists = [
          "Vegetables",
          "Meat and poultry",
          "Aquatic products",
          "Rice, noodles and beans",
          "Seasonings",
          "Fruits",
          "Other",
        ];

lists = []
def getLists():
    with open(path_ingre, encoding='utf-8')  as f_ingre:
        data_f = json.load(f_ingre)
        # 获取所有食材
        for main_class,main_ingre in data_f.items():
            for sub in main_ingre:
                for sub_class, sub_list in sub.items():
                    for key in sub_list:
                        lists.append(key)
        return lists
lists = getLists()


# 食材匹配  difflib.get_close_matches
def GetIngre(tmp):
    with open(path_ingre, encoding='utf-8') as f_ingre:
        data_f = json.load(f_ingre)
        # 食材匹配
        result = difflib.get_close_matches(tmp, lists, 1, cutoff=0.5)
        if len(result) != 0:
            # 根据匹配结果获取类别
            for key_i, value_i in data_f.items():
                for p_i in value_i:
                    for k, v in p_i.items():
                        for i in v:
                            if i == result[0]:
                                # print(k,key_i)
                                result = k,key_i
                                return list(result)
                                # print(list(result))
        else:
            result = '其他'
            return result
            # print('无匹配', tmp, result)
        # print( tmp, result)
        # return list(result)

# 3-22  食材匹配，利用Levenshtein.jaro_winkler 相似度使食材名称统一
def get_list_score(str1,str2):
    tmp = 0
    ingre = ''
    for i in str2:
        p = Levenshtein.ratio(str1, i)
        if p > tmp:
            tmp = p
            ingre = i

    # print(tmp, ingre, str2[-1])
    return [tmp,str1,ingre,str2[-1]]  # 得分， 食材名称， 同组内的标准名称

# 更新食材列表
def match_ingre(str1):
    with open(path_ingre, encoding='utf-8') as f_ingre:
        data_f = json.load(f_ingre)
        result = []
        score_list = []
        ingre_list = []
        score = 0

        # 食材匹配
        for i in lists:
            if type(i) is list:
                res1 = get_list_score(str1, i)
                score_list.append(res1[0])  # 得分
                ingre_list.append(res1[3])  # 食材
                # if res1[3]=='蛙'and p>0:
                #     print( '蛙2',str1)
            else:
                p = Levenshtein.ratio(str1, i)
                # if i=='蛙'and p>0:
                #     print( '蛙2',str1)
                score_list.append(p)
                ingre_list.append(i)
        for index, sco in enumerate(score_list):
            if sco > score:
                score = sco
                result.append(index)
        if len(result) != 0:
            ingre_match = ingre_list[result[-1]]
            if ingre_match == '蛙':
                print('蛙3', str1,score_list[result[-1]])

            for key_i, value_i in data_f.items():
                for p_i in value_i:
                    for k, v in p_i.items():
                        for item in v:
                            if ingre_match in item:

                                result_o = k,key_i
                                out_res = list(result_o)
                                # return out_res
        # print('res', score, lists[result[-1]], ingre_list[result[-1]])
        else:
            ingre_match = str1
            result_o = '其他'
            out_res = '其他'
            # return result_o
        return ingre_match  # 更新食材
        # return out_res  # 用于更新MainMaterTypes文件


# 更新MainMaterTypes文件
def get_ingre():
    lists_c = [{'川菜': 'C'}, {'徽菜': 'H'}, {'湘菜': 'X'}, {'鲁菜': 'L'}, {'闽菜': 'M'}, {'苏菜': 'S'}, {'粤菜': 'Y'}, {'浙菜': 'Z'}]
    classlist = ['chuancai','huicai','xiangcai','lucai','mincai','sucai','yuecai','zhecai']
    with open(path_m, encoding='utf-8') as m_ingre:
        data_m = json.load(m_ingre)
        res = []
        result_m = []
        p = 0
        obj = {}

        for key,value in data_m.items():
            res_n = {}
            updata_list = []



            index = 0
            index_p = lists_c[p][key]
            p = p + 1
            count_s = []
            count_t = []
            arr = []
            for dish in value:
                tmp = {}
                tmp_n = {}
                for name, ingres in dish.items():
                    # print(name,ingres)
                    tmp['id'] = index_p + str(index)
                    tmp['name'] = name
                    tmp['cate'] = classlist[p - 1]
                    res = [match_ingre(i) for i in ingres]


                    tmp_n['gid'] = str(index)
                    tmp_n['id'] = index_p + str(index)
                    tmp_n[name] = res
                    # print(tmp_n)
                    updata_list.append(tmp_n)
                    index = index + 1
            res_n[key] = updata_list   #  用于生成materialLists_new.json
            print(res_n)


        #             # result_m.append(res)
        # # print(result_m)
        #             sp = []  # 子分类
        #             tp = []  # 大分类
        #             for one in res:
        #                 if type(one) != str:
        #                     sp.append(one[0])
        #                     tp.append(one[-1])
        #                     count_t.append(one[-1])
        #                     count_s.append(one[0])
        #                 else:
        #                     sp.append(one)
        #                     tp.append(one)
        #                     count_t.append(one)
        #                     count_s.append(one)
        #             tmp['subclass'] = sp
        #             tmp['class'] = tp
        #         index = index + 1
        #         result_m.append(tmp)
        #     # 获取每个菜系使用的不同种类材料数量
        #     word_counts_t = collections.Counter(count_t)
        #     word_counts_s = collections.Counter(count_s)
        #     arr.append(dict(word_counts_t))
        #     arr.append(dict(word_counts_s))
        #     # print(arr)
        #     obj[key] = arr
        # print(obj)  # 食材出现次数统计
        # typecount_data.append(obj)
        # f_main = open('MainMaterTypes3-23.json', 'a', encoding='utf-8')
        # f_main.write(str(result_m))
        # f_main.close()

typecount_data  =[{'川菜': [{'蔬菜类': 2647, '米面豆乳类': 958, '肉禽类': 2539, '水产品类': 715, '果品类': 264, '调味品类': 2165, '药食类': 9, '其他': 2}, {'嫩茎、叶、花菜类': 130, '方便食品类': 239, '猪肉类': 1067, '豆制品': 462, '其他水产类': 146, '根茎类': 805, '牛肉类': 239, '淡水鱼': 308, '茎叶类': 657, '鸡肉类': 631, '干果类': 218, '蛋类': 171, '海水鱼': 48, '菌类': 388, '果实类': 520, '瓜菜类': 147, '其他肉类': 293, '调味品': 2148, '豆类': 111, '乳类': 12, '鸭肉类': 106, '鲜果类': 46, '米类': 58, '贝类': 82, '面、粉': 76, '食用油': 17, '羊肉类': 30, '虾类': 107, '蟹类': 24, '药食': 9, '其他': 2, '其他禽类': 2}], '徽菜': [{'蔬菜类': 237, '肉禽类': 273, '米面豆乳类': 111, '果品类': 26, '调味品类': 120, '水产品类': 112, '药食类': 5}, {'根茎类': 93, '其他肉类': 41, '猪肉类': 123, '菌类': 50, '豆制品': 49, '蛋类': 37, '干果类': 21, '调味品': 120, '海水鱼': 16, '茎叶类': 50, '面、粉': 13, '米类': 12, '淡水鱼': 52, '虾类': 18, '其他禽类': 5, '羊肉类': 4, '鸡肉类': 39, '瓜菜类': 12, '贝类': 12, '鸭肉类': 10, '方便食品类': 21, '豆类': 16, '果实类': 18, '鲜果类': 5, '药食': 5, '嫩茎、叶、花菜类': 14, '其他水产类': 12, '牛肉类': 14, '蟹类': 2}], '湘菜': [{'肉禽类': 474, '蔬菜类': 489, '调味品类': 494, '水产品类': 289, '米面豆乳类': 192, '果品类': 31, '药食类': 6}, {'牛肉类': 21, '茎叶类': 149, '调味品': 492, '淡水鱼': 95, '蛋类': 48, '猪肉类': 174, '贝类': 71, '虾类': 92, '方便食品类': 33, '根茎类': 119, '果实类': 128, '面、粉': 27, '其他肉类': 154, '豆制品': 63, '鲜果类': 19, '鸡肉类': 56, '鸭肉类': 15, '菌类': 50, '瓜菜类': 17, '嫩茎、叶、花菜类': 26, '米类': 37, '干果类': 12, '豆类': 28, '食用油': 2, '海水鱼': 19, '药食': 6, '羊肉类': 5, '蟹类': 2, '其他水产类': 10, '乳类': 4, '其他禽类': 1}], '鲁菜': [{'肉禽类': 1080, '水产品类': 708, '蔬菜类': 1103, '调味品类': 859, '药食类': 12, '米面豆乳类': 534, '果品类': 97}, {'鸡肉类': 136, '虾类': 113, '猪肉类': 552, '嫩茎、叶、花菜类': 104, '菌类': 174, '蛋类': 194, '瓜菜类': 89, '根茎类': 316, '调味品': 855, '药食': 12, '方便食品类': 119, '茎叶类': 226, '其他水产类': 117, '淡水鱼': 179, '果实类': 194, '羊肉类': 17, '豆制品': 157, '面、粉': 160, '贝类': 188, '其他肉类': 108, '牛肉类': 51, '食用油': 4, '干果类': 64, '豆类': 56, '米类': 34, '海水鱼': 96, '鲜果类': 33, '乳类': 8, '蟹类': 15, '鸭肉类': 21, '其他禽类': 1}], '闽菜': [{'肉禽类': 426, '水产品类': 199, '蔬菜类': 357, '米面豆乳类': 246, '药食类': 16, '调味品类': 206, '果品类': 60}, {'猪肉类': 190, '贝类': 90, '蛋类': 74, '淡水鱼': 24, '根茎类': 129, '面、粉': 62, '豆类': 21, '米类': 56, '其他水产类': 36, '海水鱼': 12, '菌类': 66, '药食': 16, '虾类': 32, '调味品': 205, '嫩茎、叶、花菜类': 31, '干果类': 40, '方便食品类': 59, '茎叶类': 72, '瓜菜类': 39, '果实类': 20, '鸭肉类': 13, '乳类': 4, '豆制品': 44, '其他肉类': 53, '牛肉类': 21, '鸡肉类': 60, '羊肉类': 9, '蟹类': 5, '鲜果类': 20, '食用油': 1, '其他禽类': 6}], '苏菜': [{'蔬菜类': 48, '肉禽类': 65, '水产品类': 31, '调味品类': 22, '米面豆乳类': 38, '果品类': 4}, {'根茎类': 23, '蛋类': 7, '海水鱼': 2, '猪肉类': 34, '调味品': 20, '面、粉': 15, '方便食品类': 7, '淡水鱼': 13, '果实类': 2, '其他肉类': 10, '瓜菜类': 4, '米类': 11, '茎叶类': 7, '鲜果类': 2, '蟹类': 7, '鸡肉类': 9, '菌类': 9, '虾类': 6, '食用油': 2, '鸭肉类': 5, '贝类': 1, '嫩茎、叶、花菜类': 3, '豆制品': 5, '其他水产类': 2, '干果类': 2}], '粤菜': [{'肉禽类': 2349, '蔬菜类': 2015, '调味品类': 1124, '米面豆乳类': 1551, '水产品类': 630, '果品类': 615, '药食类': 91, '其他': 1}, {'蛋类': 440, '茎叶类': 450, '调味品': 1109, '猪肉类': 902, '鸡肉类': 363, '米类': 413, '面、粉': 466, '其他肉类': 469, '虾类': 177, '根茎类': 626, '方便食品类': 257, '牛肉类': 99, '乳类': 168, '食用油': 15, '瓜菜类': 185, '其他水产类': 107, '菌类': 413, '干果类': 369, '淡水鱼': 142, '嫩茎、叶、花菜类': 176, '海水鱼': 53, '鲜果类': 246, '蟹类': 25, '贝类': 126, '药食': 91, '豆制品': 108, '果实类': 165, '豆类': 139, '羊肉类': 21, '其他禽类': 20, '鸭肉类': 35, '其他': 1}], '浙菜': [{'蔬菜类': 518, '水产品类': 248, '米面豆乳类': 311, '肉禽类': 408, '调味品类': 216, '药食类': 5, '果品类': 63}, {'茎叶类': 131, '虾类': 79, '米类': 55, '豆制品': 74, '豆类': 36, '蛋类': 85, '方便食品类': 63, '调味品': 216, '根茎类': 167, '面、粉': 78, '其他肉类': 70, '猪肉类': 183, '嫩茎、叶、花菜类': 43, '果实类': 57, '牛肉类': 20, '药食': 5, '淡水鱼': 52, '鸡肉类': 44, '干果类': 45, '海水鱼': 34, '贝类': 28, '瓜菜类': 49, '菌类': 71, '蟹类': 29, '鲜果类': 18, '乳类': 5, '其他水产类': 26, '鸭肉类': 3, '羊肉类': 2, '其他禽类': 1}]}]
# 输入为get_ingre中产生的obj
# ------------未实现--------------
def typecounts(data):
    data = data[0]
    p = 0
    cate = {}
    cate_main = []
    for cuisine,cate_class in data.items():
        # cate[citylists[p]]
        obj_m = {}
        for k,v in enumerate(cate_class[0]):
            obj_m[ingrelists[k]] = cate_class[0][v]
            # print(k,v,cate_class[0][v])
        cate_main.append((obj_m))
        cate[citylists[p]] = cate_main
        p =+1
    print(cate)



def GetInfo():
    lists = [{'川菜': 'C'}, {'徽菜': 'H'}, {'湘菜': 'X'}, {'鲁菜': 'L'}, {'闽菜': 'M'}, {'苏菜': 'S'}, {'粤菜': 'Y'}, {'浙菜': 'Z'}]
    classlist = ['chuancai','huicai','xiangcai','lucai','mincai','sucai','yuecai','zhecai']

    # 调料
    # path_s = os.getcwd() + "\\SubMaterList0.json"
    # with open(path_s,'r',encoding='utf-8') as f_s:
    #     data = json.load(f_s)
    #     result_s = []
    #     p = 0
    #     for key,value in data.items():
    #         index = 0
    #         index_p = lists[p][key]
    #         p = p + 1
    #         # cookstyleList.append(key)
    #         for dish in value:
    #             obj = {}
    #             index = index + 1
    #             for name,ingres in dish.items():
    #                 obj['id'] = index_p + str(index)
    #                 obj['name'] = name
    #                 obj['cate'] = classlist[p-1]
    #                 res = [GetIngre(i) for i in ingres]
    #                 sp = []
    #                 tp = []
    #                 for one in res:
    #                     if type(one) != str:
    #                         sp.append(one[0])
    #                         tp.append(one[-1])
    #                     else:
    #                         sp.append(one)
    #                         tp.append(one)
    #                 obj['subclass'] = sp
    #                 obj['class'] = tp
    #             # print(obj)
    #             result_s.append(obj)
    #     # print(len(result_s),result_s)
    #     f_sub = open('SubMaterTypes1.json', 'a', encoding='utf-8')
    #     f_sub.write(str(result_s))
    #     f_sub.close()

    # 主料
    path_m = os.getcwd() + "\\MainMaterList0.json"
    with open(path_m,'r',encoding='utf-8') as f_m:
        data = json.load(f_m)
        result_m = []
        p = 0
        obj = {}

        for key,value in data.items():
            index = 0
            index_p = lists[p][key]
            p = p + 1
            count_s = []
            count_t = []
            arr = []
            for dish in value:
                tmp = {}
                index = index + 1
                for name,ingres in dish.items():
                    tmp['id'] = index_p + str(index)
                    tmp['name'] = name
                    tmp['cate'] = classlist[p-1]

                    res = [GetIngre(i) for i in ingres]  # 匹配结果

                    sp = []  # 子分类
                    tp = []  # 大分类
                    for one in res:
                        if type(one) != str:
                            sp.append(one[0])
                            tp.append(one[-1])
                            count_t.append(one[-1])
                            count_s.append(one[0])
                        else:
                            sp.append(one)
                            tp.append(one)
                            count_t.append(one)
                            count_s.append(one)
                    tmp['subclass'] = sp
                    tmp['class'] = tp
                result_m.append(tmp)

            # 获取每个菜系使用的不同种类材料数量
            word_counts_t = collections.Counter(count_t)
            word_counts_s = collections.Counter(count_s)
            arr.append(dict(word_counts_t))
            arr.append(dict(word_counts_s))
            # print(arr)
            obj[key] = arr
        print(obj)
        # print(result_m)
                # result_m.append(tmp)


        f_main = open('MainMaterTypes2.json', 'a', encoding='utf-8')
        f_main.write(str(result_m))
        f_main.close()

            # print(obj)
                        # print(material,ts)
                        # try:
                        #     MainMaterList.append(GetIngre(material))
                        #     print(MainMaterList)
                        # except:
                        #     print('无匹配',item['url'])

            #         # sub_material.append(item['辅料'])
            # word_counts_taste = collections.Counter(taste)
            # print(word_counts_taste.most_common(14))
            # print(dict(word_counts_taste))

# 节点连接图
def GetJson():
    nodes = []
    links = []
    path1 = os.getcwd() + "\\MainMaterTypes2.json"
    path0 = os.getcwd() + "\\ingredients.json"

    with open(path0,'r',encoding='utf-8') as f0:
        data_f = json.load(f0)
        # 获取所有食材
        for key_i, value_i in data_f.items():
            nodes.append({'name': key_i, 'group': 2, 'class': 'ingredient_m'})
            for p_i in value_i:
                for k, v in p_i.items():
                    nodes.append({'name': k, 'group': 2, 'class': 'ingredient_s'})
                    for i in v:
                        nodes.append({'name':i,'group':2,'class':'ingredient'})
    nodes.append({'name':'其他','group':2,'class':'ingredient'})

    with open(path1,'r',encoding='utf-8') as fm:
        data = json.load(fm)
        for item in data:
            nodes.append({'id':item['id'],'name':item['name'],'group':1,'class':item['cate'],'subclass':item['subclass']})
            for i in item['subclass']:
                links.append({'relation':'食材','source':item['name'],'target':i,'value':3})

    fw = open('0106dishes.json', 'a',encoding='utf-8')
    fw.write(str({'nodes': nodes, 'links': links}))
    fw.close()


# 河流图
def GetStatistic():
    typeList = ['肉禽类', '蔬菜类','水产品类', '米面豆乳类', '调味品类', '药食类', '果品类', '其他']
    path = os.getcwd() + "\\02typecounts.json"
    with open(path, 'r', encoding='utf-8') as f:
        data_T = json.load(f)
        data = []
        res = {}
        for i in typeList:  # 遍历每个类别
            obj = {}
            obj['category'] = i
            for cate in data_T:  # 遍历菜系数据
                list_k = [k for k in data_T[cate][0]]
                if i not in list_k: # 判断该菜系是否有该类别的食材
                    obj[cate] = 0
                else:
                    for k,v in data_T[cate][0].items():
                        if i==k :
                            obj[cate] = v
            data.append(obj)
            res['data'] = data
        print(res)
        f = open('02cateriver.json','a',encoding = 'utf-8')
        f.write(str(res))
        f.close()


def test(str1,str2):
    # result = difflib.get_close_matches(str1,str2, 1, cutoff=0.5)
    # print(result)

    # 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
    sim1 = Levenshtein.distance(str1, str2)
    print('Levenshtein similarity: ', sim1)

    # 4.计算莱文斯坦比
    # 计算公式  r = (sum – ldist) / sum, 其中sum是指str1 和 str2 字串的长度总和，ldist是类编辑距离。注意这里是类编辑距离，在类编辑距离中删除、插入依然+1，但是替换+2。
    sim2 = Levenshtein.ratio(str1, str2)
    print('Levenshtein.ratio similarity: ', sim2)

    # 5.计算jaro距离
    sim3 = Levenshtein.jaro(str1, str2 )
    print('Levenshtein.jaro similarity: ', sim3)

    # 6. Jaro–Winkler距离
    sim4 = Levenshtein.jaro_winkler(str1 , str2 )
    print('Levenshtein.jaro_winkler similarity: ', sim4)

    seq = difflib.SequenceMatcher(None, str1, str2)
    ratio = seq.ratio()
    print('difflib similarity1: ', ratio)

    # for i in str2:
    #     if i in str1:
    #         print(str1)
    #         continue


str1 = '羊肉'
# str2 = '羊肚'
str2 = '羊腿肉'

# str2 = '羊排'
# test(str1,str2)

# 醋糖辣盐
def GetSubMater():
    with open(path_submater, encoding='utf-8') as f_subingre:
        data_sf = json.load(f_subingre)
        lists_t = {'甜':['糖','蜂蜜'],'咸':['盐'],'酸':['醋','柠檬'],'辣':['辣','椒']}

        for cate, dish in  data_sf.items():
            obj = {'甜':[],'咸':[],'酸':[],'辣':[]}
            for 菜 in dish:
                for 菜名, 调料列表 in 菜.items():
                    # print(菜名)
                    for 调料 in 调料列表:
                        for label, taste in lists_t.items():
                            for ts in taste:
                                if ts in 调料:
                                    # print(调料,菜名)
                                    obj[label].append(菜名)
                                    # print(obj)

            print(cate, len(obj['甜']),len(obj['咸']),len(obj['酸']),len(obj['辣']))


def GetCityLink():
    city = '/cities.json'
    climate = '/climateLinks.json'

    path = os.getcwd() + climate
    path_city = os.getcwd() + city

    city = open(path_city, 'r', encoding='utf-8')
    cityList = json.load(city)  # 需要获取信息的城市

    with open(path, 'r', encoding='utf-8') as f: # 所有城市链接
        data = json.load(f)
        for p, cities in cityList.items():
            for c in cities:
                for k, v in data.items():

                    if c == k:
                        print(p, k, v)

    city.close()


def t():

    path_c = "a.csv"
    csvfile = open(path_c, 'a', newline='', encoding='utf-8-sig')
    writer = csv.writer(csvfile)
    writer.writerow(('省份 ', '城市 ', '日期', '最高温', '最低温', '天气', '风向'))
    writer.writerow(('1', '2', '3', '4', '5'))
    csvfile.close()




if __name__ == '__main__':
    # GetInfo()
    # GetJson()
    # GetStatistic()
    # test(str1, str2)
    # GetSubMater()


    get_ingre()
    # typecounts(typecount_data)  # 未实现


    # t()
    # GetCityLink()

    # GetStatistic()
    # GetJson()
    # GetInfo()
    # GetIngre('鸡胸肉')
    pass


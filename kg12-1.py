import os,json,re,csv
import difflib
import Levenshtein
import collections,math

import demjson

cookstyleList, cuisineList, MainMaterList, tasteList = [], [], [], []
cookstyleID, cuisineID, ingredientID, tasteID = [], [], [], []
path_ingre = os.getcwd() + "/ingredients.json"
path_submater = os.getcwd() + "/SubMaterList0.json"
classlist = ['chuancai','huicai','xiangcai','lucai','mincai','sucai','yuecai','zhecai']
lists = []
def getLists():
    with open(path_ingre, encoding='utf-8')  as f_ingre:
        data_f = json.load(f_ingre)
        # 获取所有食材
        for key_i,value_i in data_f.items():
            for p_i in value_i:
                for k, v in p_i.items():
                    for i in v:
                        lists.append(i)
        return lists

lists = getLists()
#  食材匹配
def GetIngre(tmp):
    with open(path_ingre, encoding='utf-8') as f_ingre:
        data_f = json.load(f_ingre)
        # 食材匹配
        result = difflib.get_close_matches(tmp, lists, 1, cutoff=0.5)
        # print(result)

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


# 获取MainMaterTypes
def GetInfo():
    lists = [{'川菜': 'C'}, {'徽菜': 'H'}, {'湘菜': 'X'}, {'鲁菜': 'L'}, {'闽菜': 'M'}, {'苏菜': 'S'}, {'粤菜': 'Y'}, {'浙菜': 'Z'}]


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
    path_m = os.getcwd() + "\\MainMaterList3-14.json"
    with open(path_m,'r',encoding='utf-8') as f_m:
        # f_m_ = demjson.encode(f_m)
        data = json.load(f_m)
        # print(type(data))
        # data =eval(data[0])


        result_m = []
        p = 0
        obj = {}
        index_s = 0
        for key,value in data.items():
            index = 0
            index_p = lists[p][key]
            p = p + 1
            count_s = []
            count_t = []
            arr = []
            for dish in value:
                tmp = {}
                for name,ingres in dish.items():
                    tmp['gid'] = index_s

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

                index = index + 1
                index_s = index_s + 1

                result_m.append(tmp)

            # 获取每个菜系使用的不同种类材料数量
            word_counts_t = collections.Counter(count_t)
            word_counts_s = collections.Counter(count_s)
            arr.append(dict(word_counts_t))
            arr.append(dict(word_counts_s))
            # print(arr)
            obj[key] = arr
        # print(obj)
        # print(result_m)
                # result_m.append(tmp)


        f_main = open('MainMaterTypes4-8.json', 'a', encoding='utf-8')
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

# 节点链接图数据
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


def GetStatistic():
    typeList = ['肉禽类', '蔬菜类','水产品类', '米面豆乳类', '调味品类', '药食类', '果品类', '其他']
    # typeList = ['肉禽类', '蔬菜类','水产品类', '米面豆乳类', '调味品类', '果品类', '药食及其他']
    path = os.getcwd() + "\\typecounts3-14.json"
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
        # print(res)
        return res
        # f = open('cateriver3-14.json','a',encoding = 'utf-8')
        # f.write(str(res))
        # f.close()


# 3-14 合并类别，'药食类','其他'==> 其他
def combine_cate():
    catelists = ["Vegetables","Meat and poultry","Aquatic products","Rice, noodles and beans","Seasonings","Fruits","Other"]
    path = os.getcwd() + "\\typecounts3-14.json"
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        pp = []
        for key,value in data.items():
            cuisine_values = []
            tmp = {}
            for j in range(0,7):
                tmp[catelists[j]] = value[0][catelists[j]]
            cuisine_values.append(tmp)
            pp.append(cuisine_values)
        res =[]
        tmps = {}
        for i in range(0, len(classlist)):
            tmps[classlist[i]] = pp[i]
        res.append(tmps)
        print(res)

        # q = [{classlist[i]: pp[i]} for i in range(0, len(classlist))]
        # print(q)


        #     p = [{catelists[j]:value[0][catelists[j]]} for j in range(0,7)]
        #     pp.append(p)
        # # print(pp)
        # q = [{classlist[i]:pp[i]} for i in range(0,len(classlist))]
        # print(q)
        #

    pass


def test(str1,str2):
    # result = difflib.get_close_matches(str1,str2, 1, cutoff=0.5)
    # print(result)

    # 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
    sim1 = Levenshtein.distance(str1, str2)
    print('Levenshtein similarity: ', sim1)

    # 4.计算莱文斯坦比
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

    for i in str2:
        if i in str1:
            print(str1)
            continue


str1 = '鸡腿菇'
str2 = '鸡腿'
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
    GetInfo()
    # GetJson()
    # GetStatistic()
    # test(str1, str2)
    # GetSubMater()
    # GetIngre("熏肉")
    # combine_cate()
    pass
    # t()
    # GetCityLink()

    # GetStatistic()
    # GetJson()
    # GetInfo()
    # GetIngre('鸡胸肉')
import os,json,re,random

import numpy as np


path_all = os.getcwd() + "/data_combine.json"
path_ingre = os.getcwd() + "/ingredients.json"
ingre_counts = os.getcwd() + "/ingre_counts.json"
ingre_match = os.getcwd() + "/match_ingre.json"
ingre_taste = os.getcwd() + "/res.json"


lists = {
    "0": [
        {
            "ele": [
                "红枣"
            ]
        },
        {
            "rule": [
                {
                    "name": "银耳",
                    "score": 0.14814814814814814
                },
                {
                    "name": "枸杞",
                    "score": 0.2839506172839506
                }
            ]
        }
    ],
    "1": [
        {
            "ele": [
                "银耳"
            ]
        },
        {
            "rule": [
                {
                    "name": "红枣",
                    "score": 0.2
                },
                {
                    "name": "莲子",
                    "score": 0.26666666666666666
                }
            ]
        }
    ],
    "2": [
        {
            "ele": [
                "玉米淀粉"
            ]
        },
        {
            "rule": [
                {
                    "name": "猪肉",
                    "score": 0.24324324324324323
                },
                {
                    "name": "澄粉",
                    "score": 0.4324324324324324
                },
                {
                    "name": "水",
                    "score": 0.22972972972972971
                },
                {
                    "name": "鸡蛋",
                    "score": 0.24324324324324323
                },
                {
                    "name": "澄粉,猪肉",
                    "score": 0.1891891891891892
                }
            ]
        }
    ],
    "3": [
        {
            "ele": [
                "澄粉"
            ]
        },
        {
            "rule": [
                {
                    "name": "虾仁",
                    "score": 0.12380952380952381
                },
                {
                    "name": "虾",
                    "score": 0.14285714285714285
                },
                {
                    "name": "猪肉",
                    "score": 0.27619047619047615
                },
                {
                    "name": "生粉",
                    "score": 0.21904761904761905
                },
                {
                    "name": "玉米淀粉",
                    "score": 0.30476190476190473
                },
                {
                    "name": "胡萝卜",
                    "score": 0.1619047619047619
                },
                {
                    "name": "鸡蛋",
                    "score": 0.14285714285714285
                },
                {
                    "name": "糯米粉",
                    "score": 0.14285714285714285
                },
                {
                    "name": "水",
                    "score": 0.24761904761904763
                },
                {
                    "name": "粘米粉",
                    "score": 0.18095238095238095
                },
                {
                    "name": "猪肉,玉米淀粉",
                    "score": 0.13333333333333333
                },
                {
                    "name": "胡萝卜,猪肉",
                    "score": 0.11428571428571428
                }
            ]
        }
    ],
    "4": [
        {
            "ele": [
                "虾仁"
            ]
        },
        {
            "rule": [
                {
                    "name": "澄粉",
                    "score": 0.08552631578947369
                },
                {
                    "name": "猪肉",
                    "score": 0.20394736842105263
                },
                {
                    "name": "鸡蛋",
                    "score": 0.1842105263157895
                },
                {
                    "name": "胡萝卜",
                    "score": 0.09868421052631579
                }
            ]
        }
    ],
    "5": [
        {
            "ele": [
                "水"
            ]
        },
        {
            "rule": [
                {
                    "name": "肠粉专用粉",
                    "score": 0.04234527687296417
                },
                {
                    "name": "玉米淀粉",
                    "score": 0.05537459283387622
                },
                {
                    "name": "腊肉",
                    "score": 0.04234527687296417
                },
                {
                    "name": "酵母粉",
                    "score": 0.07166123778501628
                },
                {
                    "name": "澄粉",
                    "score": 0.08469055374592833
                },
                {
                    "name": "粘米粉",
                    "score": 0.08469055374592833
                },
                {
                    "name": "大米",
                    "score": 0.04560260586319218
                },
                {
                    "name": "胡萝卜",
                    "score": 0.052117263843648204
                },
                {
                    "name": "甘蔗",
                    "score": 0.04234527687296417
                },
                {
                    "name": "腊肠",
                    "score": 0.04560260586319218
                },
                {
                    "name": "香菇",
                    "score": 0.04560260586319218
                },
                {
                    "name": "面粉",
                    "score": 0.18241042345276873
                },
                {
                    "name": "白砂糖",
                    "score": 0.06188925081433224
                },
                {
                    "name": "葱",
                    "score": 0.05863192182410423
                },
                {
                    "name": "香菜",
                    "score": 0.04885993485342019
                },
                {
                    "name": "糯米粉",
                    "score": 0.1009771986970684
                },
                {
                    "name": "腌肉",
                    "score": 0.08794788273615635
                },
                {
                    "name": "生粉",
                    "score": 0.06514657980456026
                },
                {
                    "name": "蒜",
                    "score": 0.05863192182410423
                },
                {
                    "name": "姜",
                    "score": 0.1009771986970684
                },
                {
                    "name": "猪肉",
                    "score": 0.09771986970684038
                },
                {
                    "name": "鸡蛋",
                    "score": 0.1465798045602606
                },
                {
                    "name": "酵母粉,面粉",
                    "score": 0.04560260586319218
                },
                {
                    "name": "鸡蛋,面粉",
                    "score": 0.03908794788273615
                }
            ]
        }
    ],
    "6": [
        {
            "ele": [
                "肠粉专用粉"
            ]
        },
        {
            "rule": [
                {
                    "name": "水",
                    "score": 0.48148148148148145
                }
            ]
        }
    ],
    "8": [
        {
            "ele": [
                "虾"
            ]
        },
        {
            "rule": [
                {
                    "name": "澄粉",
                    "score": 0.05905511811023621
                },
                {
                    "name": "葱",
                    "score": 0.06299212598425197
                },
                {
                    "name": "蒜",
                    "score": 0.08267716535433071
                },
                {
                    "name": "姜",
                    "score": 0.10236220472440945
                },
                {
                    "name": "猪肉",
                    "score": 0.12598425196850394
                },
                {
                    "name": "胡萝卜",
                    "score": 0.08267716535433071
                },
                {
                    "name": "木耳",
                    "score": 0.05511811023622048
                },
                {
                    "name": "马铃薯",
                    "score": 0.06299212598425197
                },
                {
                    "name": "香菇",
                    "score": 0.051181102362204724
                },
                {
                    "name": "蒜,姜",
                    "score": 0.05905511811023621
                }
            ]
        }
    ],
    "10": [
        {
            "ele": [
                "猪肉"
            ]
        },
        {
            "rule": [
                {
                    "name": "澄粉",
                    "score": 0.02848722986247544
                },
                {
                    "name": "荸荠",
                    "score": 0.022593320235756383
                },
                {
                    "name": "糯米",
                    "score": 0.02455795677799607
                },
                {
                    "name": "虾仁",
                    "score": 0.030451866404715127
                },
                {
                    "name": "面粉",
                    "score": 0.05009823182711198
                },
                {
                    "name": "水",
                    "score": 0.029469548133595282
                },
                {
                    "name": "腌肉",
                    "score": 0.02455795677799607
                },
                {
                    "name": "生粉",
                    "score": 0.021611001964636542
                },
                {
                    "name": "粉丝",
                    "score": 0.02455795677799607
                },
                {
                    "name": "茄子",
                    "score": 0.030451866404715127
                },
                {
                    "name": "香菇",
                    "score": 0.0618860510805501
                },
                {
                    "name": "白菜",
                    "score": 0.023575638506876228
                },
                {
                    "name": "青椒",
                    "score": 0.03831041257367387
                },
                {
                    "name": "虾",
                    "score": 0.03143418467583497
                },
                {
                    "name": "红葱",
                    "score": 0.0206286836935167
                },
                {
                    "name": "胡萝卜",
                    "score": 0.08153241650294694
                },
                {
                    "name": "鸡蛋",
                    "score": 0.09823182711198428
                },
                {
                    "name": "葱",
                    "score": 0.06483300589390963
                },
                {
                    "name": "木耳",
                    "score": 0.0618860510805501
                },
                {
                    "name": "豆腐",
                    "score": 0.09233791748526524
                },
                {
                    "name": "葱,姜",
                    "score": 0.03241650294695481
                },
                {
                    "name": "木耳,胡萝卜",
                    "score": 0.025540275049115914
                }
            ]
        }
    ]
}

a = [{'name': "枸杞", 'score': 0.2839506172839506}, {'name': "银耳", 'score': 0.14814814814814814}]
p = ["f1", "豆腐", {'sel2_cuisine': "chuancai", 'sel2_taste': "sweet", 'sel2_level': "简单"}, {"0":"枸杞","1":"银耳"}]

list_c = 妾










3
list_t = ["sweet", "salty", "spicy", "sour", "fresh", "other"]
list_d = ['复杂','高级','普通', '简单']


def search_f3(data):
    cur_dish_gid = []  # 匹配结果索引
    if len(data[3]) >0 :
        ingres = {data[3][k] for k in data[3]}
        # print('input_ingre',ingres)  # {'枸杞', '银耳'}

        # 没有直接匹配则寻找包含某一食材的项集
        for input in data[3]:
            # ingre_rec = []  # 返回的频繁项集食材搭配
            res_match_ingre = []
            for indexs, list in lists.items():  # 频繁项集中查找
                elements = list[0]['ele']
                rules = list[1]['rule']
                if data[3][input] in elements:
                    # ingre_rec.append(elements[0])  # 若食材直接存在，则添加
                    sorted_rule = sorted(rules, key=lambda student: student['score'],
                                         reverse=True)  # 按照score值排序
                    for i in sorted_rule:
                        ingre_rec = []  # one_match
                        ingre_rec.append(elements[0])
                        ingre_rec.append(i['name'])  # 添加rule规则中的频繁项
                        res_match_ingre.append(ingre_rec)

                    # sorted_ingres = [i['name'] for i in sorted_rule]
            # print(type(ingre_rec),np.array(ingre_rec))
            # ingres_ap = {ingre for ingre in np.array(ingre_rec)}  # 判断新的食材列表是否为某一菜品食材的子集

            is_match = 0
            if len(res_match_ingre)>0:
                is_match = 1
                for item in res_match_ingre:
                    ingres_ap = {ingre for ingre in np.array(item)}
                    print('after match',ingres_ap)  # {'莲子', '银耳'}


        with open(ingre_match, encoding='utf-8') as f_ingre_match:
            match_ingre = json.load(f_ingre_match)
            for index, dish in enumerate(match_ingre):
                if ingres.issubset(dish):  # 判断输入食材列表是否为某一菜品食材的子集
                    cur_dish_gid.append(index)  # 直接返回当前食谱的id
                    # print('原有搭配',cur_dish_gid)
                elif is_match>0:
                    if ingres_ap.issubset(dish):
                        cur_dish_gid.append(index)
                        # print('关联搭配', cur_dish_gid)
            # print(cur_dish_gid)
    return cur_dish_gid

# search_f3(p)

def search_f2(data):
    sel_cuisine = data[2]['sel2_cuisine']
    sel_cuisine_index =str(list_c.index(sel_cuisine))
    sel_taste = data[2]['sel2_taste']
    sel_level = data[2]['sel2_level']
    sel_level_index = list_d.index(sel_level)
    with open(ingre_taste, encoding='utf-8') as f_f2:
        data_taste = json.load(f_f2)
        for line in data_taste:
            if line['cuisine']== sel_cuisine_index and line['cate'] == sel_taste and line['degree'] == sel_level_index:
                cur_dish_id = line['dishes']
                return cur_dish_id   # 不是gid

def search(data):
    # if data[0] == 'f3':
    #     ingres = {data[3][k] for k in data[3]}
    #     cur_dish_gid = []
    #     with open(ingre_match, encoding='utf-8') as f_ingre_match:
    #         match_ingre = json.load(f_ingre_match)
    #         for index,dish in enumerate(match_ingre):
    #             if ingres.issubset(dish):  # 判断输入食材列表是否为某一菜品食材的子集
    #                 cur_dish_gid.append(index)  # 直接返回当前食谱的id
    #             else:
    #                 # 没有直接匹配则寻找包含某一食材的项集
    #                 ingre_rec = []  # 返回的频繁项集食材搭配
    #                 for input in data[3]:
    #                     for indexs, list in lists:  # 频繁项集中查找
    #                         elements = list[0]['ele']
    #                         rules = list[1]['rule']
    #                         if data[3][input] in elements :
    #                             ingre_rec.append(elements)  # 若食材直接存在，则添加
    #                             sorted_rule = sorted(rules, key=lambda student: student['score'], reverse=True)  # 按照score值排序
    #                             for i in sorted_rule:
    #                                 ingre_rec.append(i['name'])
    #                             # sorted_ingres = [i['name'] for i in sorted_rule]
    #                             print('recommand',lists[indexs])
    #
    # elif data[0] == 'f23':
    #     ingres = {data[3][k] for k in data[3]}
    #
    #

    with open(path_all, encoding='utf-8') as f_all:
        data_all = json.load(f_all)

        id_lists = search_f2(data)
        gid_lists = search_f3(data)
        tmp = []
        res = []
        for recipe in data_all:
            if data[0] == 'f1':
                inputs = data[1]
                if recipe['name'] == inputs:
                    res.append(recipe)
                    # print('1',recipe)
            elif data[0] == 'f2':
                for id in id_lists:
                    if recipe['id'] == id:
                        res.append(recipe)
                        # print('2',recipe)
            elif data[0] == 'f3':
                for gid in gid_lists:
                    if recipe['gid'] == gid:
                        res.append(recipe)
                        # print('3',recipe)
            elif data[0] == 'f23':
                for id in id_lists:
                    if recipe['id'] == id:
                        tmp.append(recipe)
        if data[0] == 'f23':
            for gid in gid_lists:
                for item in tmp:
                    if item['gid'] == gid:
                        res.append(item)
                        # print(item)

    print(res)
    return res
    pass

# p = ["f1", "豆腐", {'sel2_cuisine': "chuancai", 'sel2_taste': "sweet", 'sel2_level': "short"}, {"0":"aaa","1":"b"}]
p = ["f3", "麻辣鱼", {'sel2_cuisine': "川", 'sel2_taste': "甜", 'sel2_level': "简单"}, {"aaa","aaaddd"}]
# print(type(p))
# search(p)

a = []
for id,va in enumerate(p):
    if id<3:
        a.append(va)
    else:
        obj ={}
        index = 0
        for item in va:
            obj[index] = item
            index =+1
        a.append(obj)
print(a)

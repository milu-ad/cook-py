


import re,json,os

path_water = os.getcwd() + "/source/water.json"
path_soil = os.getcwd() + "/source/soil.json"
# path_test = os.getcwd() + "/MainMaterTypes3-23.json"


citylists = ["川", "徽", "湘", "鲁", "闽", "苏", "粤", "浙"]
p = {"川":[], "徽":[], "湘":[], "鲁":[], "闽":[], "苏":[], "粤":[], "浙":[]}
colors3 = [
        "#3CB371",
        "#fabeba",
        "#92afed",
        "#fbecbf",
        "#f47983",
        "#ca99ef",
        "#FFA500",'#8dd3c7', '#fabeba', "#BFEFFF"
      ]


def sunburst():
    with open(path_water,'r',encoding='utf-8') as f1:
        datas = json.load(f1)
        res = []
        for j in citylists:
            res_cuisine = {}
            childWater = []
            childRiver = {}
            child = []
            childRiver['name'] = '河流'

            res_cuisine['name'] = j
            res_cuisine['itemStyle'] = {'color': colors3[citylists.index(j)]}
            valueRiver = 0
            for i in range(len(datas)):
                if datas[i]['city'] == j:
                    if datas[i]['label'] == '地表水':
                        obj_water = {}
                        obj_water['name'] = datas[i]['label']
                        obj_water['itemStyle'] = {'color': colors3[i%8]}
                        obj_water['value'] = datas[i]['labelMax']*110

                    else:
                        if datas[i]['label'] != '湖':
                            valueRiver = valueRiver + datas[i]['labelMax']
                            tmp = {}
                            tmp['name'] = datas[i]['label']
                            tmp['value'] = datas[i]['labelMax']
                            tmp['itemStyle'] = {'color': colors3[i % 6]}
                            child.append(tmp)
                        else:
                            obj = {}
                            obj['name'] = datas[i]['label']
                            obj['value'] = datas[i]['labelMax']
                            obj['itemStyle'] = {'color': 'red'}

                            childWater.append(obj)
            childRiver['value'] = valueRiver
            childRiver['children'] = child

            childWater.append(childRiver)

            obj_water['children'] =childWater
            p[j].append(obj_water)
            res_cuisine['children'] = p[j]

            res.append(res_cuisine)
        print(res)

        # for item in datas:
        #     if item.city not in citys:
        #         obj = {}
        #         childrens = []
        #         obj['name'] = item.city
        #         childrens.append(item)
        #     print(item)


    pass
# sunburst()

def bar():
    with open(path_water,'r',encoding='utf-8') as f1:
        list = ['地表水','湖','50km2','100km2','1000km2','10000km2']
        datas = json.load(f1)
        res = []
        for j in list:
            data = []
            obj = {}
            for i in range(len(datas)):
                if datas[i]['label'] == j:
                    obj['name'] = datas[i]['label']
                    obj['type'] = 'bar'
                    obj['emphasis'] = {'focus':'series'}
                    if datas[i]['label'] == '地表水':
                        value = datas[i]['labelMax']
                        obj['yAxisIndex'] = 0
                        data.append(value)
                    else:
                        obj['yAxisIndex'] = 1
                        data.append(datas[i]['labelMax'])

                    if datas[i]['label'] != '地表水' and datas[i]['label'] != '湖':
                        obj['stack'] = '河流'
            obj['data'] = data
            res.append((obj))
        print(res)

    pass
bar()
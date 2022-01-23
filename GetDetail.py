import os,json,re
import collections,math

from collections import defaultdict

# 获取菜名和主料，MainMaterList.json
def getMain():
    path = os.getcwd() + "\\data04.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        for key,value in data.items():
            tmp = {}
            arr = []
            for item in value:
                obj = {}
                MainMaterList = []
                for p in item['主料']:
                    for material,kg in p.items():
                        MainMaterList.append(material)

                if len(MainMaterList) > 0:
                    obj[item['name']] = MainMaterList
                else:
                    print(item['url'], '未添加')
                arr.append(obj)
            # print(len(arr))
            tmp[key] = arr
            # print(tmp)
            f_main = open('MainMaterList3-14.json', 'a', encoding='utf-8')
            f_main.write(str(tmp))
        f_main.close()

# 获取菜名和辅料，SubMaterList.json
def getSub():
    a = 0
    path = os.getcwd() + "\\data03.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        for key,value in data.items():
            tmp = {}
            arr = []
            for item in value:
                obj = {}
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
                    obj[item['name']] = sub_materials
                else:
                    print(item['url'], '未添加')
                arr.append(obj)
            print(len(arr))
            tmp[key] = arr
            print(tmp)
        #     f_sub = open('SubMaterList0.json', 'a', encoding='utf-8')
        #     f_sub.write(str(tmp))
        # f_sub.close()

# 获取菜名，确定种类
# 处理data02版本的菜名
def GetNameFrequence():
    path = os.getcwd() + "\\data0.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        res = []
        for key,value in data.items():
            name = []
            for item in value:
                obj = {}
                cut_list = re.split('[a-zA-Z]|正宗|版|的|自制|秘制|创新|自创', item['name'])
                if len(cut_list) > 1:
                    cut_name = cut_list[-1]
                    name.append(cut_name)
                else:
                    name.append(cut_list[0])
                word_counts_name = collections.Counter(name)
                obj[key] = dict(word_counts_name)
            # print(key,len(word_counts_name) ,dict(word_counts_name))
            res.append(obj)
            f_name = open('DishName.json', 'w', encoding='utf-8')
            f_name.write(str(res))
        f_name.close()
        return res

# 处理菜名，保存data03版本的数据，12-9
def DealName():
    obj_path = os.getcwd() + "\\data03.json"
    f1 = open(obj_path, 'a', encoding='utf-8')

    path = os.getcwd() + "\\data.json"
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        res = {}
        for key, value in data.items():
            for item in value:
                cut_list = re.split('[a-zA-Z]|正宗|版|的|自制|秘制|创新|自创', item['name'])
                if len(cut_list) > 1:
                    cut_name = cut_list[-1]
                    item['name'] = cut_name
                else:
                    item['name'] = cut_list[0]
                item['name'] = re.sub('[a-zA-Z]|家常|私房','', item['name'])
            res[key] = value
        f1.write(str(res))
    f1.close()

# 获取菜品功效
def GetEffect():
    path = os.getcwd() + "\\effect.json"
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key, value in data.items():
            print()
    pass



def GetType():
    # path = os.getcwd() + "\\DishName.json"
    # with open(path,'r',encoding='utf-8') as f:
    #     data = json.load(f)
    #     for i in range(0,len(data)):
    #         for k,v in data[i].items():
    #             for j,p in v.items():
    #                 print(j,p)

    path = os.getcwd() + "\\data03.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        res = []
        for key,value in data.items():
            name = []
            for item in value:
                print(item['name'])

# 1-18 重新整理数据
def reconstruct_data():
    index_global = 0
    lists = [{'川菜': 'C'}, {'徽菜': 'H'}, {'湘菜': 'X'}, {'鲁菜': 'L'}, {'闽菜': 'M'}, {'苏菜': 'S'}, {'粤菜': 'Y'}, {'浙菜': 'Z'}]
    classlist = ['chuancai','huicai','xiangcai','lucai','mincai','sucai','yuecai','zhecai']
    path_new = os.getcwd() + "\\data_combine.json"

    path_m = os.getcwd() + "\\data03.json"
    with open(path_m,'r',encoding='utf-8') as f_m:
        data = json.load(f_m)
        result_m = []
        p = 0
        a = 0
        for key,value in data.items():
            index = 0
            index_p = lists[p][key]
            p = p + 1
            for dish in value:
                count_m = 0
                count_f = 0
                count_p = 0
                count_t = 0
                tmp = {}
                tmp['gid'] = index_global
                tmp['id'] = index_p + str(index)
                tmp['name'] = dish['name']
                tmp['cate'] = classlist[p - 1]
                tmp['url'] = dish['url']
                tmp['main_ingre'] = dish['主料']
                count_m = len(dish['主料'])


                try:
                    if len(dish['辅料']):
                        tmp['f_ingre'] = dish['辅料']
                        count_f = len(dish['辅料'])
                except:
                    tmp['f_ingre'] = []

                try:
                    if len(dish['配料']):
                        tmp['p_ingre'] = dish['配料']
                        count_p = len(dish['配料'])
                except:
                    tmp['p_ingre'] = []

                try:
                    if len(dish['口味']):
                        tmp['taste'] = dish['口味']
                except:
                    tmp['taste'] = []

                # tmp['technics'] = dish['工艺']
                try:
                    if len(dish['工艺']):
                        tmp['technics'] = dish['工艺']
                except:
                    tmp['technics'] = []

                # tmp['time'] = dish['耗时']
                try:
                    if len(dish['耗时']):
                        tmp['time'] = dish['耗时']
                except:
                    tmp['time'] = []

                # tmp['level'] = dish['难度']
                try:
                    if len(dish['难度']):
                        tmp['level'] = dish['难度']
                except:
                    print('no level',dish('url'))
                    tmp['level'] = []

                # tmp['cooker'] = dish['厨具']
                try:
                    if len(dish['厨具']):
                        tmp['cooker'] = dish['厨具']
                except:
                    tmp['cooker'] = []

                # tmp['step'] = dish['步骤']
                try:
                    if len(dish['步骤']):
                        tmp['step'] = dish['步骤']
                        count_t = len(dish['步骤'])
                except:
                    tmp['step'] = []

                count = count_m + count_f + count_p + count_t    # 食材和步骤复杂度

                index = index + 1
                index_global = index_global + 1
                result_m.append(tmp)
                # print(tmp)

        # f_main = open(path_new, 'a', encoding='utf-8')
        # f_main.write(str(result_m))
        # f_main.close()


if __name__ == '__main__':
    getMain()
    # getSub()
    # GetType()
    # GetNameFrequence()
    # DealName()
    # reconstruct_data()
    pass
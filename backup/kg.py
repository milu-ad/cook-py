import os,json,re
import difflib

cookstyleList, cuisineList, MainMaterList, tasteList = [], [], [], []
cookstyleID, cuisineID, ingredientID, tasteID = [], [], [], []
path_ingre = os.getcwd() + "/ingredients.json"

def GetIngre(tmp):
    with open(path_ingre, encoding='utf-8')  as f_ingre:
        data_f = json.load(f_ingre)
        for key_i,value_i in data_f.items():
            for p_i in value_i:
                for k, v in p_i.items():
                    #  匹配方案一
                    res = difflib.get_close_matches(tmp, v, 2, cutoff=0.3)
                    if len(res) != 0:
                        print(res,k,key_i)
                        result = key_i
                        return result
                        # break
                    else:
                        print('无匹配', tmp)

                # for k,v in p_i.items():
                #     # if re.findall(tmp, str(v)):
                #     #     q = re.findall(tmp, str(v))
                #     pattern = re.compile(str(v))
                #     if pattern.findall(tmp):
                #         q = pattern.findall(tmp)
                #
                #         # q = re.findall(str(v), tmp)
                #         print(q,k,key_i)
                #         return k
                #     else:
                #         print('无匹配',tmp)

def GetInfo():
    path = os.getcwd() + "\\data.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        for key,value in data.items():
            cookstyleList.append(key)
            for item in value:
                tasteList.append(item['口味'])
                cuisineList.append(item['name'])
                for p in item['主料']:
                    for material,kg in p.items():
                        print(material)
                        # try:
                        #     MainMaterList.append(GetIngre(material))
                        #     print(MainMaterList)
                        # except:
                        #     print('无匹配',item['url'])


            #         # sub_material.append(item['辅料'])
            # word_counts_taste = collections.Counter(taste)
            # print(word_counts_taste.most_common(14))
            # print(dict(word_counts_taste))
# GetInfo()
GetIngre('虾肉棒')
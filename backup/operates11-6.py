import json,jieba
import re,json,os

arr = []


list1 = ['川菜','徽菜','晋菜','鲁菜','闽菜','苏菜','粤菜','浙菜']

# for item in list1:
#     path = os.getcwd() + "/"+ item +".json"
#     with open(path,encoding='utf-8')  as f:
#         data = json.load(f)
#         for line in data:
#             print(line)
#         print(len(data))

path = os.getcwd() + "/闽菜.json"
foods = os.getcwd() + "/food.txt"

def GetWords():
        with open(path,encoding='utf-8')  as f:
            data = json.load(f)
            print(len(data))
            arr = {}
            for line in data:
                # p = re.sub(r'[【】\-\—~]+', ' ', line['name'])
                # p = re.sub(r'#信任之美#【闽菜】[【】\--\—\：~]+', ' ', line['name'])
                # 去除英文字符
                zhList = re.sub(r'[a-zA-Z]','',line['name'])
                # q = re.split('。|！|？|#|【|】|-|~|～|—|－|＠|（|）|，|：|=|的| |“|”',a)
                # 按照非中文字符划分
                spList = re.split(r'[^\u4e00-\u9fa5]',zhList)
                lists = [i for i in spList if i != '']
                arr[line['url']] = lists
            #with open('fooooo.txt', 'a', encoding='utf-8') as fs:
            fs=open('fooooo.txt', 'a', encoding='utf-8')
            for i in arr:
                tmp = []
                # 按照菜名词库匹配
                if len(arr[i]) == 1:
                    # 常规菜名
                    # print(type(arr[i][0]),arr[i][0])
                    cl_names = re.sub(r'独家','',arr[i][0])
                    # print(type(cl_names),cl_names)
                    obj = {}
                    count = 0
                    # tmp.append([count,arr[i]])
                    obj['count'] = count
                    # obj[name] = arr[i][0]
                    tmp.append(obj)
                    print("\n".join(jieba.lcut(cl_names,cut_all = False)))
                    fs.write("\n".join(jieba.lcut(cl_names,cut_all = False)))
            fs.close()




def GetClearIni():
    foodLists = []
    with open(foods, encoding='utf-8') as f1:
        lines = f1.readlines()
        for line in lines:
            res = re.split('\t', line)
            foodLists.append(res[0])

    with open(path,encoding='utf-8')  as f:
        data = json.load(f)
        print(len(data))
        arr = {}
        for line in data:
            # p = re.sub(r'#信任之美#【闽菜】[【】\--\—\：~]+', ' ', line['name'])
            # 去除英文字符
            zhList = re.sub(r'[a-zA-Z]','',line['name'])
            # q = re.split('。|！|？|#|【|】|-|~|～|—|－|＠|（|）|，|：|=|的| |“|”',a)
            # 按照非中文字符划分
            spList = re.split(r'[^\u4e00-\u9fa5]',zhList)
            lists = [i for i in spList if i != '']
            arr[line['url']] = lists

        for i in arr:
            tmp = []
            # 按照菜名词库匹配
            if len(arr[i]) == 1:
                # 常规菜名
                obj = {}
                count = 0
                # tmp.append([count,arr[i]])
                obj['count'] = count
                # obj[name] = arr[i][0]
                tmp.append(obj)


            else:
                for j in range(0, len(arr[i])):
                    count = 0
                    # print(i,lists[i])
                    for food in foodLists:
                        obj = {}
                        if re.findall(food, arr[i][j]):
                            p = re.findall(food, arr[i][j])
                            # print(j,p,arr[i][j])
                            count += 1
                            # tmp.append([count,arr[i][j]])
                            obj['count'] = count
                            obj['name'] = arr[i][j]
                            tmp.append(obj)
                            # print(i,count)
                            continue
                    # if count
                    # if len(tmp) > 1:
                    #     maxNum = max(tmp)
            # print(tmp)

def GetClear():
    with open(path, encoding='utf-8')  as f:
        data = json.load(f)
        with open('clear_1.txt','r',encoding='utf-8') as f2:
            datas = f2.readlines()
            for i in range(0,len(data)):
                # print(len(eval(datas[i])))
                listLen = len(eval(datas[i]))
                list_cut = eval(datas[i])
                # print(list_cut)
                if listLen > 1:
                    tmp = 0
                    num = [j['count'] for j in eval(datas[i])]
                    set_num = set(num)
                    if len(set_num) != 1:
                        # 判断list中元素是否完全相同
                        for k in range(0,listLen):
                            if list_cut[k]['count'] > tmp:
                                tmp = list_cut[k]['count']
                                data[i]['name'] = list_cut[k]['name']
                    else:
                        print(i, data[i]['name'], '无匹配')
                    # print(i, data[i]['name'])

                elif listLen == 0:
                    # data[i]['name'] = data[i]['name']
                    print(i,data[i]['name'],'无匹配')
                else:
                    if list_cut[0]['count'] == 1:
                        data[i]['name'] = list_cut[0]['name']

                print(i, data[i]['name'])

if __name__ == '__main__':
    GetWords()
    # GetClear()
    # GetClearIni()
    pass


# with open(path, encoding='utf-8')  as f:
#     data = json.load(f)
#
#     for i in range(0,len(data)):
#         print(tmp[i]['count'])
            # if tmp[i]['count'] == 0
            # line[i].name =

        # if len(tmp) == 0:
        #     errorList.append(i)
        # elif len(tmp) > 1:
        #     if
        #     dishName = tmp[-1]
        #     print(dishName)



        # if len(lists) > 1:
        #     for i in range(0,len(lists)):
        #         arr = []
        #         for food in foodLists:
        #             if re.findall(lists[i], food):
        #                 # p = lists[i].search(food)
        #                 p = re.findall(lists[i], food)
        #                 print(i,p,line['name'])
        #                 name.append(lists[i])
        #                 arr.append(lists[i])
        #                 continue
        #             else:
        #                 count = len(re.findall(lists[i],food))
        #                 print(count)
        #
        #     if len(arr) == 0:
        #         # print(lists)
        #         name.append(lists)
        # else:
        #     name.append(lists[0])
        # # print(name)


        # for item in q:
        #     if re.findall(item,foodLists):
        #         name = re.findall(item,foodLists)
        #         print(item,name)
        #     else:
        #         print(item,'none')
        #

        # p = jieba.cut(line['name'])
        # print(line['name'],'/'.join(p))


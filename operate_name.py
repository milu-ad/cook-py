import json,jieba
import re,json,os

arr = []
list1 = ['川菜','徽菜','湘菜','鲁菜','闽菜','苏菜','粤菜','浙菜']

path = os.getcwd() + "/小吃川1.json"
foods = os.getcwd() + "/food.txt"

def GetWords():
    # 新增词汇写入词库
        with open(path,encoding='utf-8')  as f:
            data = json.load(f)
            print(len(data))
            arr = {}
            for line in data:
                # p = re.sub(r'[【】\-\—~]+', ' ', line['name'])
                # p = re.sub(r'#信任之美#【闽菜】[【】\--\—\：~]+', ' ', line['name'])
                # 去除英文字符
                zhList = re.sub(r'[a-zA-Z]|的做法|独家|和配方','',line['name'])
                # q = re.split('。|！|？|#|【|】|-|~|～|—|－|＠|（|）|，|：|=|的| |“|”',a)
                # 按照非中文字符划分
                spList = re.split(r'[^\u4e00-\u9fa5]',zhList)
                lists = [i for i in spList if i != '']
                arr[line['url']] = lists
            #with open('fooooo.txt', 'a', encoding='utf-8') as fs:

            y = []
            for i in arr:
                tmp = []
                # 按照菜名词库匹配
                if len(arr[i]) == 1:
                    # 常规菜名
                    # print(type(arr[i][0]),arr[i][0])
                    cl_names = re.sub(r'独家','',arr[i][0])
                    # cl_names = re.sub(r'的做法', '', cl_names)
                    # print(type(cl_names),cl_names)
                    obj = {}
                    count = 0
                    # tmp.append([count,arr[i]])
                    obj['count'] = count
                    # obj[name] = arr[i][0]
                    tmp.append(obj)
                    # print("\n".join(jieba.lcut(cl_names,cut_all = False)))
                    # if len()

                    for k in jieba.lcut(cl_names,cut_all = False):
                        y.append(k)

            # print(tmp)
            q = set(y)
            with open('food.txt', 'a', encoding='utf-8') as fs:
                sw = open('stop.txt', 'r', encoding='utf-8')
                stopwords = []
                for word in sw:
                    word = re.sub("\n",'',word)
                    stopwords.append(word)
                sw.close()
                for g in q:
                    if g not in stopwords:
                        print(g)
                        fs.write(g+'\n')


def GetClearIni():
    foodLists = []
    with open(foods, encoding='utf-8') as f1:
        lines = f1.readlines()
        for line in lines:
            res = re.split('\t', line)
            foodLists.append(res[0])
        foodLists = set(foodLists)

    with open(path,encoding='utf-8')  as f:
        data = json.load(f)
        print(len(data))
        arr = {}
        for line in data:
            zhList = re.sub(r'[a-zA-Z]|的做法|独家|和配方','',line['name'])
            spList = re.split(r'[^\u4e00-\u9fa5]',zhList)
            lists = [i for i in spList if i != '']
            arr[line['url']] = lists

        for i in arr:
            tmp = []
            ft = open('clear_12.txt', 'a', encoding='utf-8')
            # 按照菜名词库匹配
            if len(arr[i]) == 1:
                # 常规菜名
                obj = {}
                count = 0
                obj['count'] = count
                # obj[name] = arr[i][0]
                tmp.append(obj)
                # print(tmp)
            else:
                for j in range(0, len(arr[i])):
                    count = 0
                    for food in foodLists:
                        obj = {}
                        food = re.sub("\n",'',food)
                        if re.findall(food, arr[i][j]):
                            p = re.findall(food, arr[i][j])
                            # print(j,p,arr[i][j])
                            count += 1
                            # tmp.append([count,arr[i][j]])
                            obj['count'] = count
                            obj['name'] = arr[i][j]
                            tmp.append(obj)
                            continue
            # print(tmp)
            ft.write(str(tmp) + '\n')
        ft.close()
        print('菜品名划分完成')

def GetClear():
    with open(path, encoding='utf-8')  as f:
        data = json.load(f)
        with open('clear_12.txt','r',encoding='utf-8') as f2:
            f_new = open('川菜2.json','w',encoding='utf-8')
            datas = f2.readlines()
            res = []
            print(len(data),len(datas))
            for i in range(0,len(data)):
                # print(len(eval(datas[i])))
                listLen = len(eval(datas[i]))
                list_cut = eval(datas[i])
                # print(list_cut)
                data[i]['name'] = re.sub(r'[a-zA-Z]|的做法|独家|和配方|又叫|又名|首发', '', data[i]['name'])
                data[i]['name'] = re.split(r'[^\u4e00-\u9fa5]', data[i]['name'])
                if listLen > 1:
                    tmp = 0
                    num = [j['count'] for j in eval(datas[i])]
                    set_num = set(num)
                    if len(set_num) != 1:
                        # 判断list中元素是否完全相同
                        for k in range(0,listLen):
                            if list_cut[k]['count'] > tmp:
                                tmp = list_cut[k]['count']
                                data[i]['name'] = str(list_cut[k]['name'])
                            else:
                                print(i, data[i]['name'], '频率相同，无匹配')
                    # else:
                    #     print(i, data[i]['name'], '仅一个匹配')
                elif listLen == 0:
                    print(i,data[i]['name'],'无匹配')
                else:
                    if list_cut[0]['count'] == 1:
                        data[i]['name'] = list_cut[0]['name']
                # print( data[i]['name'])
                res.append(data[i])
            f_new.write(str(res))
            f_new.close()
                # print(i, data[i]['name'])

if __name__ == '__main__':
    # GetWords()
    # GetClearIni()
    GetClear()
    pass


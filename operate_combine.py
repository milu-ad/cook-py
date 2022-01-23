import os,json


list1 = ['川菜','徽菜','湘菜','鲁菜','闽菜','苏菜','粤菜','浙菜']

# obj_path = os.getcwd() + "\\data.json"
# f1 = open(obj_path, 'a', encoding='utf-8')

def MergeTypeData():
    # res = []
    for item in list1:
        nums = [0,1]
        res = []
        fpath = os.getcwd() + "\\f" + item + ".json"
        f2 = open(fpath, 'a', encoding='utf-8')
        for i in nums:
            obj_path = os.getcwd() + "\\"+item+str(i)+".json"
            f1 = open(obj_path, 'r', encoding='utf-8')

            data = json.load(f1)
            count = 0

            for line in data:
                if line not in res:
                    if isinstance(line['name'],list):
                        line['name'] = line['name'][0]
                    res.append(line)
            f1.close()
        f2.write(str(res))
        f2.close()
        print(item)

#  去重
def Dedul():
    path = os.getcwd() + "/四川小吃.json"

    f1 = open(path, 'r', encoding='utf-8')
    datas = json.load(f1)
    res = []
    with open('小吃川1.json', 'a', encoding='utf-8') as fw:
        for data in datas:
            if data not in res:
                print(data['url'])
                res.append(data)
        fw.write(str(res) + '\n')


# 菜系数据汇总
def GetAllData():
    obj_path = os.getcwd() + "\\data.json"
    f1 = open(obj_path, 'a', encoding='utf-8')

    res = {}
    obj = {}
    for item in list1:
        path = os.getcwd() + "\\"+item+"0.json"
        arr = []
        # obj = {}
        with open(path,encoding='utf-8')  as f:
            data = json.load(f)
            count = 0
            num_dish = len(data)
            # with open('stop.txt', 'r', encoding='utf-8') as sw:
            #     lines = sw.readlines()
            #     for line in lines:
            #         stopwords = re.sub("\n",'',line)
            #         stopLists.append(stopwords)

            for line in data:
                if line in arr:
                    print(line)
                    continue
                elif isinstance(line['name'],list):
                    line['name'] = line['name'][0]
                    arr.append(line)
                else:
                    arr.append(line)

            obj[item] = arr

    f1.write(str(obj))
            # res.push(obj)
    # 修改数据格式

    # print(res)
    # f1.write(str(res))
    f1.close()


if __name__ == '__main__':
    # MergeTypeData()
    # Dedul()
    GetAllData()
    pass



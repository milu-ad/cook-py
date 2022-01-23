import json, time, csv
import re, requests, json, os

from itertools import islice
from bs4 import BeautifulSoup

# 爬取城市天气年平均值数据
# 按照菜系所在省会求取平均值


path_city = os.getcwd() + "\\cities.json"
path_city_num = os.getcwd() + "\\historyLinks.json"
path_w = os.getcwd() + "\\4-14ClimateData.json"
path_clear_data = os.getcwd() + "/cliamte_cleardata_before.json"

def GetData(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    time.sleep(2)
    print(url)
    res = requests.get(url,headers = headers)
    soup = BeautifulSoup(res.content.decode("utf-8"), "html.parser")
    re = str(soup)
    # print(re)
    data = re.split('=', 1)[1]
    if data[0] != '{':
        return
    else:
        return json.loads(data)


url = 'https://j.i8tq.com/history/stationData/{}.json?_='

lists = ['101220101','101221601', '101220101']
t = []
# for address in lists:
#     p = GetData(url.format(address))
#     t.append(p)
#     print(t)
#     print(p)


# 获取所有天气数据
def getLink():
    # with open(path_city,'r',encoding='utf-8') as f:
    #     data = json.load(f)
    #     for cuisine in data:
    #         # print(cuisine,data[cuisine])
    #         for city in data[cuisine]:
    #             print(city)
    with open(path_city_num, 'r', encoding='utf-8') as f_1:
        city_data = json.load(f_1)
        datas = city_data['城市代码']
        url = 'https://j.i8tq.com/history/stationData/{}.json?_='
        f = open(path_w,'w',encoding = 'utf-8')
        obj = {}
        for line in datas:
            tmp = []
            cityLists = line['市']
            for item in cityLists:
                city_code = item['编码']
                data = GetData(url.format(city_code))
                tmp.append(data)
            obj[line['省']] = tmp
        # print(obj)
        f.write(str(obj))
        f.close()


# getLink()

# 计算平均值
def calculate(data):
    res = []
    tmp={}
    for i in range(0,12):
        tmp[i] = 0
        for line in data:
            tmp[i] = int(line[i]) + tmp[i]
        # res.append(round(tmp[i]/12,2))
        res.append(int(tmp[i]/len(data)))
        # print(res)
    return res


def avgData():
    with open(path_w,'r',encoding='utf-8') as f:
        data_all = json.load(f)
        res = {}
        for cuisine,datas in data_all.items():
            obj = {}
            yearAvgTemp,yearAvgRainDay,yearMinTemp,yearAvgRain,yearMaxTemp,yearAvgHumidity = [],[],[],[],[],[]
            for line in datas:
                cityDatas = list(line.values())
                cityData = cityDatas[0]
                # 整合每个省市的所有城市数据
                yearAvgTemp.append(cityData['yearAvgTemp'])
                yearAvgRainDay.append(cityData['yearAvgRainDay'])
                yearMinTemp.append(cityData['yearMinTemp'])
                yearAvgRain.append(cityData['yearAvgRain'])
                yearMaxTemp.append(cityData['yearMaxTemp'])
                yearAvgHumidity.append(cityData['yearAvgHumidity'])
            # 计算平均值
            obj['yearAvgTemp'] = calculate(yearAvgTemp)
            obj['yearAvgRainDay'] = calculate(yearAvgRainDay)
            obj['yearMinTemp'] = calculate(yearMinTemp)
            obj['yearAvgRain'] = calculate(yearAvgRain)
            obj['yearMaxTemp'] = calculate(yearMaxTemp)
            obj['yearAvgHumidity'] = calculate(yearAvgHumidity)
            res[cuisine] = obj
        f = open(path_clear_data, 'w',encoding='utf-8')
        f.write(str(res))
        f.close()

avgData()
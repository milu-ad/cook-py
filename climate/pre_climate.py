import os,json

# 将kg4-13_clamate.py 文件中产生的天气数据转换为视图所需格式


path_iniData = os.getcwd() + "/pre_cliamte_temp.json"
path_new_data = os.getcwd() + "/cliamte_cleardata_before.json"
path_clear_data = os.getcwd() + "/pre_cliamte_cleardata.json"
path_clear_data_city = os.getcwd() + "/pre_cliamte_cleardata_city.json"
#  成都 安徽合肥 长沙 济南   福建福州  江苏南京  广州  浙江杭州


citylist = [{ '川菜': 'C' }, { '徽菜': 'H' }, { '湘菜': 'X' }, { '鲁菜': 'L' }, { '闽菜': 'M' }, { '苏菜': 'S' }, { '粤菜': 'Y' }, { '浙菜': 'Z' }]
citylists = ['chuancai', 'huicai', 'xiangcai', 'lucai', 'mincai', 'sucai', 'yuecai', 'zhecai']
lists = ['C', 'H', 'X', 'L', 'M', 'S', 'Y', 'Z']
def climate_data():
    with open(path_new_data,'r',encoding='utf-8') as f_data:
        data_all = json.load(f_data)
        res = []
        index = 0;
        for city, data in data_all.items():
            for i in range(0, 12):
                print(data)

                obj = {}
                obj['city'] = city
                obj['cityid'] = lists[index]
                obj['id'] = lists[index]+'m'+str(i+1)
                for indicator, value in data.items():
                    if indicator == 'yearAvgTemp':
                        obj['yearAvgTemp'] = value[i]
                    if indicator == 'yearMinTemp':
                        obj['yearMinTemp'] = value[i]
                    if indicator == 'yearMaxTemp':
                        obj['yearMaxTemp'] = value[i]
                    if indicator == 'yearAvgHumidity':
                        obj['yearAvgHumidity'] = value[i]
                    if indicator == 'yearAvgRain':
                        obj['yearAvgRain'] = value[i]
                    if indicator == 'yearAvgRainDay':
                        obj['yearAvgRainDay'] = value[i]
                    # if indicator == 'SeasonAvgTmin':
                    #     obj['SeasonAvgTmin'] = value[i]
                    # if indicator == 'SeasonAvgRain':
                    #     obj['SeasonAvgRain'] = value[i]
                    # if indicator == 'SeasonAvgTmax':
                    #     obj['SeasonAvgTmax'] = value[i]
                res.append(obj)
            index += 1
        print(len(res),res)
        f = open(path_clear_data, 'w',encoding='utf-8')
        f.write(str(res))
        f.close()
climate_data()
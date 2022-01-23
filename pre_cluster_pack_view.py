# -*- coding: utf-8 -*-
import os,json,csv
import numpy as np
import pandas as pd

path_allData = os.getcwd() + "/01result01.csv"
path_new = os.getcwd() + "/01PackData.json"
path_new_pollu = os.getcwd() + "/0604PackData.json"

classlist = ['chuancai', 'huicai', 'xiangcai', 'lucai', 'mincai', 'sucai', 'yuecai', 'zhecai']
cluster_type_num = 8

def get_datas():

    with open(path_allData,'r',encoding='utf-8') as f_all:
        reader = csv.reader(f_all)
        result = list(reader)
        print(result)
        index_lists = [1,3487,3846,4720,6616,7179,7273,10305,11039]
        child_fir = []
        num = []
        nums = [result[i][3] for i in range(1,len(result)) if result[i][3] not in num]
        # print(list(set(nums)))   #['4', '2', '0', '6', '1', '5', '7', '3']
        types = list(set(nums))

        res = {"name":"cuisine","children":[]}


        for k in range(0,len(classlist)):
            layer = get_construct_data(index_lists[k], index_lists[k+1], k,types, result)
            child_fir.append(layer)
        res['children'] = child_fir
        f_main = open(path_new, 'a', encoding='utf-8')
        f_main.write(str(res))
        f_main.close()
        print('完成')


        # layer = get_construct_data(index_lists[0], index_lists[1], 0, types, result)
        # f_main = open(path_new, 'a', encoding='utf-8')
        # f_main.write(str(layer))
        # f_main.close()

def get_construct_data(i,j,k,types,result):
    obj_sec = {}
    obj_third = {}
    obj_sec['name'] = classlist[k]
    child_all_type = []
    obj_third['name'] = 'all_types'

    child_third = []
    for t in range(0,len(types)):
        child_out = {}
        child_out['name'] = 'type'+types[t]   # name:'typea',children:[]
        child_list = []  # 最里层children
        for p in range(i, j):
            child_item = {}
            if result[p][3] == types[t]:
                child_item['index'] = result[p][0]
                child_item['size'] = 1
                child_item['cate'] = result[p][3]
                child_list.append(child_item)
            child_out['children'] = child_list
        child_third.append(child_out)
        # print(child_third)
    obj_third['children'] = child_third
    child_all_type.append(obj_third)
    obj_sec['children'] = child_all_type
    # print(obj_sec)
    return obj_sec

        # csv_data = pd.read_csv(f_all)
        # print(type(csv_data))
        # q = []
        # for row in f1:
        #     p = {}
        #     p = row
        #     q.append(p)
        # print(type(q),q)


# get_datas()



path_allData = os.getcwd() + "/CO.json"
path_new = os.getcwd() + "/01PackData.json"

classlists = ["北部沿海", "东部沿海", "东北", "南部沿海", "黄河中游", "长江中游", "西南地区", "大西北地区"]
lists = [["北京市", "天津市", "河北省", "山东省"],["上海市", "江苏省", "浙江省"],["辽宁省", "吉林省", "黑龙江省"],
 ["福建省", "广东省", "海南省", "香港", "台湾省"],["山西省", "内蒙古自治区", "河南省", "陕西省"],["安徽省", "江西省", "湖北省", "湖南省"],
 ["广西壮族自治区", "重庆市", "四川省", "贵州省", "云南省"],["西藏自治区", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区"]]

cluster_type_num = 5


sequence_index = [1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
cityLists =["上海市", "临沧市", "丽江市", "保山市", "大理白族自治州", "德宏傣族景颇族自治州", "怒江傈僳族自治州", "文山壮族苗族自治州", "昆明市", "昭通市", "普洱市", "曲靖市", "楚雄彝族自治州", "玉溪市", "红河哈尼族彝族自治州", "西双版纳傣族自治州", "迪庆藏族自治州", "乌兰察布市", "乌海市", "兴安盟", "包头市", "呼伦贝尔市", "呼和浩特市", "巴彦淖尔市", "赤峰市", "通辽市", "鄂尔多斯市", "锡林郭勒盟", "阿拉善盟", "北京市", "云林县", "南投县", "台东县", "台中市", "台北市", "台南市", "嘉义县", "基隆市", "宜兰县", "屏东县", "彰化县", "新北市", "新竹县", "桃园市", "花莲县", "苗栗县", "高雄市", "吉林市", "四平市", "延边朝鲜族自治州", "松原市", "白城市", "白山市", "辽源市", "通化市", "长春市", "乐山市", "内江市", "凉山彝族自治州", "南充市", "宜宾市", "巴中市", "广元市", "广安市", "德阳市", "成都市", "攀枝花市", "泸州市", "甘孜藏族自治州", "眉山市", "绵阳市", "自贡市", "资阳市", "达州市", "遂宁市", "阿坝藏族羌族自治州", "雅安市", "天津市", "中卫市", "吴忠市", "固原市", "石嘴山市", "银川市", "亳州市", "六安市", "合肥市", "安庆市", "宣城市", "宿州市", "池州市", "淮北市", "淮南市", "滁州市", "芜湖市", "蚌埠市", "铜陵市", "阜阳市", "马鞍山市", "黄山市", "东营市", "临沂市", "威海市", "德州市", "日照市", "枣庄市", "泰安市", "济南市", "济宁市", "淄博市", "滨州市", "潍坊市", "烟台市", "聊城市", "菏泽市", "青岛市", "临汾市", "吕梁市", "大同市", "太原市", "忻州市", "晋中市", "晋城市", "朔州市", "运城市", "长治市", "阳泉市", "东莞市", "中山市", "云浮市", "佛山市", "广州市", "惠州市", "揭阳市", "梅州市", "汕头市", "汕尾市", "江门市", "河源市", "深圳市", "清远市", "湛江市", "潮州市", "珠海市", "肇庆市", "茂名市", "阳江市", "韶关市", "北海市", "南宁市", "崇左市", "来宾市", "柳州市", "桂林市", "梧州市", "河池市", "玉林市", "百色市", "贵港市", "贺州市", "钦州市", "防城港市", "乌鲁木齐市", "五家渠市", "伊犁哈萨克自治州", "克孜勒苏柯尔克孜自治州", "克拉玛依市", "北屯市", "博尔塔拉蒙古自治州", "双河市", "可克达拉市", "吐鲁番市", "和田地区", "哈密市", "喀什地区", "图木舒克市", "塔城地区", "巴音郭楞蒙古自治州", "昆玉市", "昌吉回族自治州", "石河子市", "胡杨河市", "铁门关市", "阿克苏地区", "阿勒泰地区", "阿拉尔市", "南京市", "南通市", "宿迁市", "常州市", "徐州市", "扬州市", "无锡市", "泰州市", "淮安市", "盐城市", "苏州市", "连云港市", "镇江市", "上饶市", "九江市", "南昌市", "吉安市", "宜春市", "抚州市", "新余市", "景德镇市", "萍乡市", "赣州市", "鹰潭市", "保定市", "唐山市", "廊坊市", "张家口市", "承德市", "沧州市", "石家庄市", "秦皇岛市", "衡水市", "邢台市", "邯郸市", "三门峡市", "信阳市", "南阳市", "周口市", "商丘市", "安阳市", "平顶山市", "开封市", "新乡市", "洛阳市", "济源市", "漯河市", "濮阳市", "焦作市", "许昌市", "郑州市", "驻马店市", "鹤壁市", "丽水市", "台州市", "嘉兴市", "宁波市", "杭州市", "温州市", "湖州市", "绍兴市", "舟山市", "衢州市", "金华市", "万宁市", "三亚市", "东方市", "临高县", "乐东黎族自治县", "五指山市", "保亭黎族苗族自治县", "儋州市", "定安县", "屯昌县", "文昌市", "昌江黎族自治县", "海口市", "澄迈县", "琼中黎族苗族自治县", "琼海市", "白沙黎族自治县", "陵水黎族自治县", "仙桃市", "十堰市", "咸宁市", "天门市", "孝感市", "宜昌市", "恩施土家族苗族自治州", "武汉市", "潜江市", "神农架林区", "荆州市", "荆门市", "襄阳市", "鄂州市", "随州市", "黄冈市", "黄石市", "娄底市", "岳阳市", "常德市", "张家界市", "怀化市", "株洲市", "永州市", "湘潭市", "湘西土家族苗族自治州", "益阳市", "衡阳市", "邵阳市", "郴州市", "长沙市", "临夏回族自治州", "兰州市", "嘉峪关市", "天水市", "定西市", "平凉市", "庆阳市", "张掖市", "武威市", "甘南藏族自治州", "白银市", "酒泉市", "金昌市", "陇南市", "三明市", "南平市", "厦门市", "宁德市", "泉州市", "漳州市", "福州市", "莆田市", "龙岩市", "山南市", "拉萨市", "日喀则市", "昌都市", "林芝市", "那曲市", "阿里地区", "六盘水市", "安顺市", "毕节市", "贵阳市", "遵义市", "铜仁市", "黔东南苗族侗族自治州", "黔南布依族苗族自治州", "黔西南布依族苗族自治州", "丹东市", "大连市", "抚顺市", "朝阳市", "本溪市", "沈阳市", "盘锦市", "营口市", "葫芦岛市", "辽阳市", "铁岭市", "锦州市", "阜新市", "鞍山市", "重庆市", "咸阳市", "商洛市", "安康市", "宝鸡市", "延安市", "榆林市", "汉中市", "渭南市", "西安市", "铜川市", "果洛藏族自治州", "海东市", "海北藏族自治州", "海南藏族自治州", "海西蒙古族藏族自治州", "玉树藏族自治州", "西宁市", "黄南藏族自治州", "香港", "七台河市", "伊春市", "佳木斯市", "双鸭山市", "哈尔滨市", "大兴安岭地区", "大庆市", "牡丹江市", "绥化市", "鸡西市", "鹤岗市", "黑河市", "齐齐哈尔市"]

def get_construct_data_pollution(k,types,result):
    obj_sec = {}
    obj_third = {}
    obj_sec['name'] = classlist[k]

    child_all_type = []
    obj_third['name'] = 'all_types'

    child_third = []
    for t in range(0,len(types)):
        child_out = {}
        child_out['name'] = 'type'+ str(t)   # name:'typea',children:[]
        child_list = []  # 最里层children
        for p in range(384):
            if sequence_index[p] == k:
                child_item = {}
                # print(result[p]['cate'])
                if result[p]['cate'] == types[t]:
                    child_item['index'] = result[p]['id']
                    child_item['size'] = 1
                    child_item['city'] = cityLists[p]
                    child_item['cate'] = result[p]['cate']
                    child_list.append(child_item)
                # print(child_list)
                child_out['children'] = child_list
        child_third.append(child_out)


        # print(child_third)
    obj_third['children'] = child_third
    child_all_type.append(obj_third)

    obj_sec['children'] = child_all_type
    # print(obj_sec)
    return obj_sec


def get_datas():

    with open(path_allData,'r',encoding='utf-8') as f_all:
        jsonStr = json.load(f_all)
        result = jsonStr['201301']
        # print(result)
        child_fir = []
        nums = [0,1,2,3,4]
        res = {"name":"country","children":[]}


        for k in range(0,len(classlists)):
            layer = get_construct_data_pollution(k,nums, result)
            child_fir.append(layer)

        # res['children'] = child_fir
        # f_main = open(path_new_pollu, 'a', encoding='utf-8')
        # f_main.write(str(res))
        # f_main.close()
        # print('完成')

# print(len(sequence_index))  # 384

# sequences= {'上海市': 1, '云南省': 6, '内蒙古自治区': 4, '北京市': 0, '台湾省': 3, '吉林省': 2, '四川省': 6, '天津市': 0, '宁夏回族自治区': 7, '安徽省': 5, '山东省': 0, '山西省': 4, '广东省': 3, '广西壮族自治区': 6, '新疆维吾尔自治区': 7, '江苏省': 1, '江西省': 5, '河北省': 0, '河南省': 4, '浙江省': 1, '海南省': 3, '湖北省': 5, '湖南省': 5, '甘肃省': 7, '福建省': 3, '西藏自治区': 7, '贵州省': 6, '辽宁省': 2, '重庆市': 6, '陕西省': 4, '青海省': 7, '香港': 3, '黑龙江省': 2}
# print()



# get_datas()


path_seq = os.getcwd() + '/sequence.txt'
def get_sequence():
    with open(path_seq, 'r', encoding='utf-8') as f:
        jsonStr = json.load(f)
        res = {}
        res_se = []
        for i,v in enumerate(jsonStr):
            prov = jsonStr[i].split('-')[0]
            city = jsonStr[i].split('-')[1]
            for j in lists:
                if prov in j:
                    res[city] = lists.index(j)
                    res_se.append(city)
        print(res_se)
        # print(jsonStr)
        pass
# get_sequence()




# path_new = os.getcwd() + "/KeyjsonIAQI_city_addProv.json"
def getValue(json_name, nowdate):
    print(json_name, nowdate)
    # filenames = json_name.split(',')
    # dates = nowdate.split(',')
    filenames = json_name
    dates = nowdate

    directory = "D:\\2021VIS\\ChinaVis2021\\flask\\static\\KeyjsonIAQI_city_addProv"  # json文件所在的目录路径
    # json文件所在的目录路径

    result = []
    oneday = {}
    onedayDt = []
    res = {}

    for root, dirs, files in os.walk(directory):
        for f in files:
            fpath = os.path.join(root, f)
            fname, fename = os.path.split(fpath)
            for filename in filenames:

                if (filename + '.json') == fename:
                    print(filename)
                    with open(fname + '\\' + fename, encoding='utf-8') as fw:
                        jsonStr = json.load(fw)
                        onecityDay = {}
                        p = []

                        for dt in dates:
                            oneCity = {}
                            onecityDay[dt] = jsonStr[dt]
                            p.append(jsonStr[dt])
                    res[filename] = p
                    # result.append(res)
                    # print(res)
    # for city,value in data.items():
    # print(res)
    result = []
    obj = {}
    levels = [1, 3, 5, 7, 9, 11]
    influs = ['B', 'C', 'D', 'E', 'F', 'G']
    for i in range(len(dates)):
        day = []

        for city, value in res.items():
            # print(city,value)
            tmp = {}
            tmp[city] = value[i]
            value[i]['Influ'] =  levels[influs.index(value[i]['Influ'])]
            day.append(tmp)
        obj[dates[i]] = day
        result.append(obj)
    print(obj)

    return result
    # print(oneday)
    #

    # return json.dumps(result)
city_s =["上海市", "临沧市"]
# data = getValue(city_s,['2013-01-01','2013-01-02'])


def changeDay(data,city_s,time):
    print()
    obj={}
    for dt in time:
        day = []
        for city,value in data.items():
            tmp = {}
            # tmp[city] = value[0][dt]
            day.append(value[0][dt])
            print(value[0][dt])
        obj[dt] = day

    print(obj)
    pass
# changeDay(data,city_s,['2013-01-01','2013-01-02'])


def changeType(data, city_s, time):
    print()
    obj = {}
    for dt in time:
        day = []
        for city, value in data.items():
            tmp = {}
            tmp['name'] = value[0][dt][city]
            tmp['IAQI'] = value[0][dt]['IAQI']
            tmp['cityCode'] = value[0][dt]['adcode']
            tmp['value'] = levels[influs.index(value[0]['Influ'])]
            day.append(tmp)
        obj[dt] = day

    print(obj)
    pass


def addview():
    pathC = os.getcwd() + "/CO.json"
    path_new = os.getcwd() + "/01PackData.json"
    pass





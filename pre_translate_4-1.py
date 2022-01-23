import os,json,re,random
import hashlib,time, http
from urllib import parse

path_all = os.getcwd() + "/data_combine.json"
path_ingre = os.getcwd() + "/ingredients.json"
ingre_counts = os.getcwd() + "/ingre_counts.json"
ingre_match = os.getcwd() + "/match_ingre.json"



# 中文翻译成英文
def translate_t(myurl, httpClient, q_t):
    fromLang = 'auto'  # 原文语种[自动检测]
    toLang = 'en'  # 译文语种[英语]
    salt = random.randint(32768, 65536)
    sign = appid + q_t + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl1 = myurl + '?appid=' + appid + '&q=' + parse.quote(
        q_t) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl1)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        jg = (result['trans_result'][0]['dst'])
    except Exception as e:
        print(e)
        jg = '接口请求出错'
    finally:
        if httpClient:
            httpClient.close()
    return jg


# 英文翻译成中文
def translate_f(myurl, httpClient, q_f):
    fromLang = 'auto'  # 原文语种[自动检测]
    toLang = 'zh'  # 译文语种[中文]
    salt = random.randint(32768, 65536)
    sign = appid + q_f + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl1 = myurl + '?appid=' + appid + '&q=' + parse.quote(
        q_f) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl1)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        jg = (result['trans_result'][0]['dst'])
    except Exception as e:
        print(e)
        jg = '接口请求出错'
    finally:
        if httpClient:
            httpClient.close()
    return jg


# 获取ingre_counts中的中文食材,存入一个字符串
def get_info_cn():
    with open(ingre_counts, encoding='utf-8') as f_ingre:
        data_ingre = json.load(f_ingre)
        res = {}
        all = []
        for cuisine,ingreList in data_ingre.items():
            ingres = []
            for line in ingreList[0]:
                all.append(line)
                ingres.append(line)
            res[cuisine] = ingres
        return res
        print(res)
# get_info_cn()

# 将翻译结果进行字符串分割
def get_info_en(texts):
    res = {}
    # 将中文时才按照菜系拼接称字符串
    for key, value in texts.items():
        a = ''
        for j in value:
            a = a + '，' + j
        i = a[1:]
        print(len(i),i)
        news = []
        if 'img' not in i and i != '':
            httpClient = None
            myurl = '/api/trans/vip/translate'
            q_t = i.replace('<p>', '')
            q_f = translate_t(myurl, httpClient, q_t)
            # 将翻译结果(str)按照'-'分割并存为数组
            print(q_f)
            p = re.split(',', q_f)
            print(len(p),p)
            res[key] = p

            time.sleep(5)
            # jg = translate_f(myurl, httpClient, q_f)
            # time.sleep(5)
            # print('<p>' + jg)
            # news.append('<p>' + jg)
        else:
            news.append(i)

    with open(ingre_counts, encoding='utf-8') as f_ingre:
        data_ingre = json.load(f_ingre)
        res_n = {}
        all = []
        for cuisine,ingreList in data_ingre.items():
            ingres = []
            obj = {}
            print(len(ingreList[0]))
            for index,value in enumerate(ingreList[0]):
                obj[res[cuisine][index]] = ingreList[0][value]
                ingres.append(obj)
                # print(index,value,ingreList[0][value],obj[res[cuisine][index]])
            res_n[cuisine] = ingres
        print(res_n)



def trans(i):
    news = []
    if 'img' not in i and i != '':
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q_t = i.replace('<p>', '')
        time.sleep(3)
        q_f = translate_t(myurl, httpClient, q_t)
        # print(q_f,type(q_f))
        time.sleep(2)
        # jg = translate_f(myurl, httpClient, q_f)
        # time.sleep(5)
        # print('<p>' + jg)
        # news.append('<p>' + jg)
    else:
        news.append(i)
    return q_f

def new_trans():
    with open(ingre_counts, encoding='utf-8') as f_ingre:
        data_ingre = json.load(f_ingre)
        res_n = {}
        for cuisine,ingreList in data_ingre.items():
            ingres = []
            obj = {}
            for index, value in enumerate(ingreList[0]):
                trans_res = trans(value)
                obj[trans_res] = ingreList[0][value]
                print(obj)
            ingres.append(obj)
            res_n[cuisine] = obj

    fw = open('ingre_counts_en-4_1.json', 'a',encoding='utf-8')
    fw.write(str(res_n))
    fw.close()



if __name__ == '__main__':
    # 测试用
    i = '苦瓜,辣椒，香蕉,辣椒,菜薹'  # 需要翻译的字符串

    news = []
    if 'img' not in i and i != '':
        appid = '20210331000755658'  # 填写你的appid
        secretKey = 'O6OVgBhaTnvPlngC_37k'  # 填写你的密钥
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q_t = i.replace('<p>', '')
        q_f = translate_t(myurl, httpClient, q_t)
        # print(q_f,type(q_f))
        time.sleep(5)
        # jg = translate_f(myurl, httpClient, q_f)
        # time.sleep(5)
        # print('<p>' + jg)
        # news.append('<p>' + jg)
    else:
        news.append(i)
    print(q_f,type(q_f))
    p = re.split(',',q_f)
    print(p,type(p))




    # appid = '20210331000755658'  # 填写你的appid
    # secretKey = 'O6OVgBhaTnvPlngC_37k'  # 填写你的密钥
    # new_trans()


    #
    # texts = get_info_cn()
    # get_info_en(texts)

    # res = {}
    # for key,value in texts.items():
    #     a = ''
    #     for j in value:
    #         a = a + ','+j
    #     i = a[1:]
    #
    #     news = []
    #     if 'img' not in i and i != '':
    #         appid = '20210331000755658'  # 填写你的appid
    #         secretKey = 'O6OVgBhaTnvPlngC_37k'  # 填写你的密钥
    #         httpClient = None
    #         myurl = '/api/trans/vip/translate'
    #         q_t = i.replace('<p>', '')
    #         q_f = translate_t(myurl, httpClient, q_t)
    #         print(q_f)
    #         res[key] = q_f
    #
    #         time.sleep(5)
    #         # jg = translate_f(myurl, httpClient, q_f)
    #         # time.sleep(5)
    #         # print('<p>' + jg)
    #         # news.append('<p>' + jg)
    #     else:
    #         news.append(i)
    # print(res)
import requests,os,json,re
from bs4 import BeautifulSoup

# 读取词条，记录食材名称

path_ingre = os.getcwd() + "/ingredients.json"

# 获取百度词条食材标准名称
with open(path_ingre, encoding='utf-8') as f_ingre:
    data_f = json.load(f_ingre)
    res =[]
    main_obj = {}
    main_ingres = []
    for mainclass,line_m in data_f.items():
        sub_obj = {}
        tmp = []
        for subclass, line_s in line_m[0].items():
            sub_ingres =[]
            not_match = []
            matches = []  # 记录所有匹配的名称以及别名

            for ingre in line_s:
                link = 'https://baike.baidu.com/item/'+ ingre
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"
                }
                response = requests.get(link,headers = headers)
                soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
                # print(soup)
                div = soup.find('div','basic-info cmn-clearfix')
                alias =[]  # 别名
                try:
                    if div.find_all('dd'):
                        dd = div.find_all('dd')
                        dt = div.find_all('dt')
                        chineseName = div.find('dd').text.replace('\n', '').replace(' ','')

                        if len(dd) > 1:
                            for i in range(0,len(dt)):
                                if dt[i].text == '别    名':
                                # dd[1].text.replace('\n', '').split('，')  数组
                                    names = dd[i].text.replace('\n', '')
                                    spList = re.split(r'[^\u4e00-\u9fa5]', names)   # 以非中文字符划分
                                    cut_res = [j for j in spList if j !='']    # 去除空元素
                                    for k in cut_res:
                                        # print(k)
                                        if k not in matches:
                                            matches.append(k)
                                    alias = cut_res
                                    # alias = dd[i].text.replace('\n', '').split('，')
                        if chineseName != ingre:
                            alias.append(ingre)
                            matches.append(chineseName)
                        matches.append(ingre)
                        alias.append(chineseName)

                        sub_ingres.append(alias)

                except:
                    not_match.append(ingre)
                    # print('no match',ingre)
                    # sub_ingres.append(ingre)
                    continue

            for item in not_match:  #
                if item in matches:
                    continue
                else:
                    sub_ingres.append([item])
            # print(sub_ingres)
            # print('match', matches)

            # exit()
            sub_obj[subclass] = sub_ingres
        tmp.append(sub_obj)
        main_obj[mainclass] = tmp
        print(main_obj)
    main_ingres.append(main_obj)
    print(main_ingres)

#





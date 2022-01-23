import jieba,os,json,re
import collections,math

from collections import defaultdict
import jieba.posseg as pseg
import jieba.analyse as anls

list1 = ['川菜','徽菜','湘菜','鲁菜','闽菜','苏菜','粤菜','浙菜']

# 确定口味

def TopicMining():
    res = []
    path = os.getcwd() + "\\data.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        for p in data:
            taste = []
            sub_material = []
            for key, value in p.items():
                for item in value:
                    taste.append(item['口味'])
                    # sub_material.append(item['辅料'])

            word_counts_taste = collections.Counter(taste)
            print(word_counts_taste.most_common(14))
            # print(dict(word_counts_taste))

def taste(k1,b):
    path = os.getcwd() + "\\data.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        doc_num = len(data)

        list_words = []
        doc_frequency=[]
        lists = []
        dish = []
        len_taste_ini = []
        for key,value in data.items():
            taste = []
            obj = {}
            dish.append(key)
            for item in value:
                taste.append(item['口味'])
            len_taste_ini.append(len(taste))
            lists_s = set(taste)
            lists.append(lists_s)

            obj[key] = taste
            word_counts_taste = collections.Counter(taste)
            list_words.append(obj)

            frequency = dict(word_counts_taste)
            doc_frequency.append(frequency)

            # tmp[key] = frequency
            # doc_frequency.append(tmp)
        print(len_taste_ini)
        p = 0
        for i in range(0,len(len_taste_ini)):
            p = p+len_taste_ini[i]
        avgdl = p/8   # 文档D中所有文档的平均长度


        word_tf = {}
        word_idf = {}  # 存储每个词的idf值

        bm_idf = {}
        bm_r = {}
        arr=[]
        brr = []
        for i in range(0,len(doc_frequency)):

            word_tf_idf = {}
            word_bm25 = {}

            word_doc = defaultdict(int)  # 存储包含该词的文档数
            for k,v in doc_frequency[i].items():
                word_tf[k] = v / sum(doc_frequency[i].values())
                for j in range(0, len(lists)):
                    if k in lists[j]:
                        word_doc[k] += 1
                # print(k,word_doc[k])
                word_idf[k] = math.log(doc_num / (word_doc[k] + 1))
                word_tf_idf[k] = word_tf[k] * word_idf[k]

                bm_idf[k] = math.log(doc_num - word_doc[k] + 0.5 / (word_doc[k] + 0.5))
                bm_r[k] = v * (k1 + 1) / (v + k1 * (1 - b + b * len_taste_ini[i] / avgdl))
                word_bm25[k] = bm_idf[k]*bm_r[k]

            brr.append(word_bm25)
            arr.append(word_tf_idf)
            # print(word_tf_idf)

        print(arr)
        print(brr)
        print()
        for i in range(0,len(arr)):
            ret = max(arr[i], key=lambda x: arr[i][x])
            ret_b = max(brr[i], key=lambda x: brr[i][x])

            print(dish[i], ret, arr[i][ret])
            print(dish[i], ret_b, brr[i][ret_b])


if __name__ == '__main__':
    taste(1.2,0.75)
    pass


    #         if isinstance(line['name'],list):
    #             dishName = line['name'][0]
    #         else:
    #             dishName = line['name']
    #         # wordsCut = jieba.lcut(dishName,cut_all = False)
    #
    #         for k in jieba.lcut(str(dishName),cut_all = False):
    #             if k not in stopLists:
    #                 words.append(k)
    #     word_counts = collections.Counter(words)
    #     word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
    #     print(word_counts_top10)  # 输出检查
    #     words.append(obj)
    # print(obj)
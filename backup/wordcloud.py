import jieba,os,json,re
import collections,math

from collections import defaultdict
import jieba.posseg as pseg
import jieba.analyse as anls

list1 = ['川菜','徽菜','湘菜','鲁菜','闽菜','苏菜','粤菜','浙菜']


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

def taste():
    path = os.getcwd() + "\\data.json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
        doc_num = len(data)

        list_words = []
        doc_frequency=[]
        lists = []
        for key,value in data.items():
            taste = []
            obj = {}
            tmp = {}
            for item in value:
                taste.append(item['口味'])
            lists_s = set(taste)

            lists.append(lists_s)
            obj[key] = taste
            word_counts_taste = collections.Counter(taste)
            list_words.append(obj)

            frequency = dict(word_counts_taste)
            doc_frequency.append(frequency)

            # tmp[key] = frequency
            # doc_frequency.append(tmp)

        word_tf = {}
        word_idf = {}  # 存储每个词的idf值
        word_doc = defaultdict(int)  # 存储包含该词的文档数
        word_tf_idf = {}

        for i in range(0,len(doc_frequency)):
            for k,v in doc_frequency[i].items():
                word_tf[k] = v / sum(doc_frequency[i].values())
                for j in lists[i]:
                    if k in lists[i]:
                        word_doc[k] += 1
            print(word_doc)

        # for one in doc_frequency:
        #     for keys,lists in one.items():
        #         for k,v in lists.items():
        #             if k in list_words:
        #                 word_doc[k] += 1
        #     print(word_doc)

        # for i in doc_frequency:
        #     word_tf[i] = doc_frequency[i] / sum(doc_frequency.values())
        #     for li in list_words:
        #         for k,v in li.items():
        #             if i in v:
        #                 word_doc[i] += 1
        #
        # print(word_doc)
            # doc_frequency = {}
            # for k,v in dict(word_counts_taste).items():
            #     doc_frequency[k] = v
            # print(doc_frequency)
            #
            # word_idf = {}  # 存储每个词的idf值
            # word_doc = defaultdict(int)  # 存储包含该词的文档数
            # word_tf = {}
            # word_tf_idf = {}
            # for i in doc_frequency:
            #     word_tf[i] = doc_frequency[i] / sum(doc_frequency.values())
            #     for li in list_words:
            #         for j,v in li.items():
            #             if i in v:
            #                 word_doc[i] += 1
            # print(word_doc)
            # for i in doc_frequency:  # 计算idf
            #     word_idf[i]=math.log(doc_num/(word_doc[i]+1))
            #
            # for i in doc_frequency:  # 计算tf_idf
            #     word_tf_idf[i] = word_tf[i] * word_idf[i]

            # print(li,word_tf_idf)

        # doc_frequency = {}
        # for k,v in dict(word_counts_taste).items():
        #     doc_frequency[k] = v
        # print(doc_frequency)
        word_idf = {}  # 存储每个词的idf值
        word_doc = {}  # 存储包含该词的文档数
        word_tf = {}
        word_tf_idf = {}
        # for i in doc_frequency:
        #     word_tf[i] = doc_frequency[i] / sum(doc_frequency.values())
        #     for j,v in list_words.items():
        #         if i in v:
        #             word_doc[i] += 1
        # for i in doc_frequency:  # 计算idf
        #     word_idf[i]=math.log(doc_num/(word_doc[i]+1))
        #
        # for i in doc_frequency:  # 计算tf_idf
        #     word_tf_idf[i] = word_tf[i] * word_idf[i]

        print()













if __name__ == '__main__':
    taste()
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
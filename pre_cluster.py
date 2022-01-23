# -*- coding:utf-8 -*-


import os,json,jieba
import numpy as np
import jieba.posseg as pseg
import jieba.analyse as anls
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import Birch
from sklearn.cluster import KMeans
import collections
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from scipy.spatial.distance import cdist  # 计算距离
from sklearn import metrics

path_allData = os.getcwd() + "/data05.json"
path_new_data = os.getcwd() + "/data_combine.json"
path_main_types = os.getcwd() + "/MainMaterTypes3-23.json"




lists = [{'川菜': 'C'}, {'徽菜': 'H'}, {'湘菜': 'X'}, {'鲁菜': 'L'}, {'闽菜': 'M'}, {'苏菜': 'S'}, {'粤菜': 'Y'}, {'浙菜': 'Z'}]
classlist = ['chuancai', 'huicai', 'xiangcai', 'lucai', 'mincai', 'sucai', 'yuecai', 'zhecai']

lists_t = ['微辣','中辣','超辣','麻辣','酸辣','甜辣','香辣','酸甜','酸咸','咸鲜','咸甜','甜味','苦味','原味','清淡','五香','鱼香','葱香','蒜香','奶香','酱香','糟香','咖喱','孜然','果味','香草','怪味','咸香','甜香','麻香','其他']
lists_w = ['烧','炒','爆','焖','炖','蒸','煮','拌','烤','炸','烩','溜','氽','腌','卤','炝','煎','酥','扒','熏','煨','酱','煲','烘焙','火锅','砂锅','拔丝','生鲜','调味','技巧','烙','榨汁','冷冻','焗','焯','干煸','干锅','铁板','微波','其他']
lists_h = ['十分钟','廿分钟','半小时','三刻钟','一小时','数小时','一天','数天']

center_points = []
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})

class pre_cluster:
    def __init__(self):
        self.title_dict = {}
        self.cluster_dict = {}
        self.y_kmeans = {}
        pass

    # 统计原材料数目以及步骤数作为菜品复杂度
    def hard_level(self):
        with open(path_allData,'r',encoding='utf-8') as f_all:
            data = json.load(f_all)
            res = []
            s = 0
            m=0
            h=0
            t=0
            for cate, info in data.items():
                for dish in info:
                    count_m = 0
                    count_f = 0
                    count_p = 0
                    count_t = 0
                    for k,v in dish.items():
                        if k == '主料':
                            count_m = len(v)
                        if k == '辅料':
                            count_f = len(v)
                        if k == '配料':
                            count_p = len(v)
                        if k == '步骤':
                            count_t = len(v)
                    count = count_m + count_f  + count_p + count_t
                    if count<20:
                        s+=1
                    elif count<40:
                        m+=1
                    elif count<60:
                        h+=1
                    else:
                        t +=1

                    res.append(count)
            print(res)
            print()
            print(np.max(res),np.min(res))
            print(s,m,h,t)
            return res

    # 记录出现的食材
    def record_words(self, value, lists):
        for li in value:
            if list(li.keys())[0] not in lists:
                lists.append(list(li.keys())[0])
        return lists

    # 食材汇总时去重
    def combine_words(self,list1,list2,list3):
        res = []
        # for j in range(1,4):
        res = [i for i in list1 if i not in res]
        res.extend([i for i in list2 if i not in res])
        res.extend([i for i in list3 if i not in res])
        print(len(res), res)
        return res

    def record_tool(self, value, lists):
        for li in value:
            if li not in lists:
                lists.append(li)

    # 步骤处理
    # 合并一道菜的步骤
    def combine_step(self,lists_steps):

        combine_steps, tmp = [], []
        a = 0
        if len(lists_steps) == 0:
            return
        else:
            for step in lists_steps:
                if '成品图' in step and len(step) < 7:
                    a = a + 1
                else:
                    # 合并一道菜的所有步骤
                    tmp = str(tmp) + '，' + step
        combine_steps.append(tmp[3:])
        # print('combine_steps',combine_steps)  #['煮熟牛肉丸和腊排骨。 炒香。 ，拌一下。 然后放入其他配菜。，煮几分钟放入适量盐和味精。，捞出，热油放干辣椒炸一下淋上即可。']
        return combine_steps

    # 合并所有菜的步骤
    def combine_steps(self,dish_steps):
        res,verb_words = [],[]

        for dish in dish_steps:
            combine_steps = []
            tmp = []
            a = 0
            if len(dish) == 0:
                return
            else:
                for step in dish:
                    if '成品图' in step and len(step) < 7:
                        a = a + 1
                    else:
                        # 合并一道菜的所有步骤
                        tmp = str(tmp) + '，' + step
            combine_steps.append(tmp[3:])

        # print('combine_steps', combine_steps)
            words = pseg.cut(combine_steps[0])
            for word, flag in words:
                if flag == 'v':
                    verb_words.append(word)
        print('all_verb_words', verb_words)

        return verb_words

    # 获取所有动词，筛出前200高频词
    def filter_words(self, verb_words):
        # 统计词频 筛选前200
        # print(verb_words[0])

        fre_words = [ '翻炒','煮','切', '搅拌', '腌制', '焯', '撒', '煎',  '拌匀',
                      '炸', '焖', '爆香','浸泡', '煮开', '炖', '泡','炒香', '切碎', '烧',
                      '腌','剁', '煸', '浇', '抓', '蒸', '拌','加水', '煮熟','调',
                      '包','抹','烫','煲', '淋', '蒸好', '铺', '擀', '烤', '淋入',
                      '裹', '勾芡', '煮沸', '揉', '蒸熟','熬', '翻', '晾凉', '拍','打',
                      '爆炒', '放凉', '沾', '蘸','搓',  '汆', '打散', '控干', '发酵','斩', '剪',
                      ]
        lists_w = ['烧', '炒', '爆', '焖', '炖', '蒸', '煮', '拌', '烤', '炸', '烩', '溜', '氽', '腌', '卤', '炝', '煎', '酥', '扒', '熏',
                   '煨', '酱', '煲', '烘焙', '火锅', '砂锅', '拔丝', '生鲜', '调味', '技巧', '烙', '榨汁', '冷冻', '焗', '焯', '干煸', '干锅', '铁板',
                   '微波', '其他']

        q1 = collections.Counter(verb_words).most_common(200)
        resu = dict(q1)
        print(resu)
        words_f = [k for k in resu.keys()]
        # output = ' '.join(['%s' % x for x in words_f]).encode('utf-8')
        output = ' '.join(['%s' % x for x in words_f])

        print(output)
        # corpus.append(output.strip())
        # return output

    def cut_words(self, corpus, step, verb_words):

        # 默认直接分词
        # seg_list = jieba.cut(step[0], cut_all=False)
        # # output = ' '.join(['%s' % x for x in list(seg_list)]).encode('utf-8')
        # output = ' '.join(['%s' % x for x in list(seg_list)])
        # 分词后只留动词

        high_fre_words = ['放入','加入','倒入','翻炒','洗净','煮','放','备用','适量','加','准备','出','切','料酒','捞出','切成','炒','搅拌','腌制','是','去','焯','撒','下入','开','煎','烧热','盖','要','烧开','到','拌匀','干','炸','吃','焖','继续','开水','有','爆香','放在','浸泡','煮开','炖','泡','入','取出','倒','切好','炒香','匀','待用','炒锅','清洗','洗','取','入味','切碎','烧','做','出来','会','起锅','腌','炒出','调入','炒匀','待','转','剁','让','煸','浇','喜欢','可','加盐','盛出','抓','蒸','拌','加水','煮熟','放进','熟','炒至','做好','没有','成','调','加热','入锅','提前','包','抹','使','烫','去掉','来','煲','开始','剁成','起来','起','淋','蒸好','备','捞起','铺','炒好','好吃','处理','留','擀','即','烤','淋入','不用','裹','放到','能','勾芡','成热','烧至','完成','买','搅匀','需要','煮沸','揉','蒸熟','没','去除','熬','剁碎','撒入','炒熟','翻','装入','注意','晾凉','拍','如','变','调好','放进去','剩下','盛入','料','适量水','打','加盖','盛','爆炒','改','面糊','转中','放凉','沾','拿','选择','蘸','凉','打开','不能','捞','铺上','预热','搓','注入','留底','摆盘','调成','汆','享用','粘','冷却','打散','发','出锅','熟透','烹入','直到','沸腾','控干','剩余','断生','进','看','生','调味料','斩','剪','发酵','加上','分成','反复','揉成','进行','叉烧','滚']

        high_fre_words = ['翻炒', '煮', '切', '搅拌', '腌制', '焯', '撒', '煎', '拌匀',
                     '炸', '焖', '爆香', '浸泡', '煮开', '炖', '泡', '炒香', '切碎', '烧',
                     '腌', '剁', '煸', '浇', '抓', '蒸', '拌', '加水', '煮熟', '调',
                     '包', '抹', '烫', '煲', '淋', '蒸好', '铺', '擀', '烤', '淋入',
                     '裹', '勾芡', '煮沸', '揉', '蒸熟', '熬', '翻', '晾凉', '拍', '打',
                     '爆炒', '放凉', '沾', '蘸', '搓', '汆', '打散', '控干', '发酵', '斩', '剪',
                     ]
        words = pseg.cut(step[0])
        res = []
        for word, flag in words:
            if flag == 'v':
                if word in high_fre_words:
                    res.append(word)
                    verb_words.append(word)

        if len(res) == 0:
            res = []

        # return verb_words
        output = ' '.join(['%s' % x for x in res])
        corpus.append(output.strip())
        # print('corpus',corpus)
        # if flag == True:
        #     f = open('verb-1-15.txt','w',encoding='utf-8')
        #     f.write(corpus)
        #     f.close()
        return corpus

    def tfidf1(self,corpus):
        # for x, w in anls.textrank(step, withWeight=True):
        #     print('%s %s' % (x, w))

        # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer()
        # 该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()
        # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        cipin = vectorizer.fit_transform(corpus)
        pq = cipin.toarray()
        print(cipin.shape, cipin.toarray()) # 矩阵(11038, 30745)

        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

        # 获取词袋模型中的所有词语
        word = vectorizer.get_feature_names()
        # print(word)

        # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        self.weight = tfidf.toarray()
        # print(self.weight)

        # resCipin = os.getcwd() + "/OneCipin_Result.txt"
        # result = open(resCipin, 'a', encoding='utf-8')
        # for j in range(len(word)):
        #     result.write(word[j] + ' ')
        # result.write('\r\n\r\n')
        # for i in range(len(pq)):
        #     # print(u"-------这里输出第", i, u"类文本的词语词频------")
        #     for j in range(len(word)):
        #         result.write(str(pq[i][j]) + ' ')
        #     result.write('\r\n\r\n')


        # resName = os.getcwd() + "/0newTfidf_Result.txt"
        # result = open(resName, 'a', encoding='utf-8')
        # for j in range(len(word)):
        #     result.write(word[j] + ' ')
        # result.write('\r\n\r\n')
        #
        # # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        # for i in range(len(self.weight)):
        #     print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        #     for j in range(len(word)):
        #         result.write(str(self.weight[i][j]) + ' ')
        #     result.write('\r\n\r\n')

        # result.close()

    def get_cipin(self,corpus):
        # for x, w in anls.textrank(step, withWeight=True):
        #     print('%s %s' % (x, w))

        # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        # vectorizer = CountVectorizer(token_pattern=r'(?u)\b\w+\b')  # 步骤-保留单个字符，默认为字符长度需大于2
        vectorizer = CountVectorizer(token_pattern=r'(?u)\b[\S]+\b')  # 主料-保留非空白字符 \S，\s是空白字符

        # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        cipin = vectorizer.fit_transform(corpus)
        # print('cipin',cipin)
        # print(cipin.shape, cipin.toarray()) # 矩阵(11038, 30745)

        # 获取词袋模型中的所有词语，列表形式呈现文章生成的词典
        word = vectorizer.get_feature_names()

        # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        self.weight = cipin.toarray()
        # print("词频矩阵大小", self.weight,len(word),word)

        resName = os.getcwd() + "/ingre_weight_01-15-8-1.txt"
        result = open(resName, 'a', encoding='utf-8')
        #
        # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        for i in range(len(self.weight)):
            # print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
            for j in range(len(word)):
                result.write(str(self.weight[i][j]) + ' ')
            result.write('\r\n')

    def get_matrixs(self, corpus, value):
        lists_sub_class = ['嫩茎、叶、花菜类', '方便食品类', '猪肉类', '豆制品', '其他水产类', '根茎类', '牛肉类', '贝类', '淡水鱼', '茎叶类', '鸡肉类', '干果类', '蛋类', '菌类', '果实类', '虾类', '蟹类', '其他', '其他肉类', '调味品', '瓜菜类', '乳类', '米类', '其他禽类', '鸭肉类', '海水鱼', '鲜果类', '面、粉', '豆类', '药食', '羊肉类', '食用油','其他']
        res = []
        for item in value:
            if item in lists_sub_class:
                res.append(item)
        if len(res) == 0:
            res = []
        output = ' '.join(['%s' % x for x in res]).encode('utf-8')
        # output = ' '.join(['%s' % x for x in res])
        corpus.append(output.strip())
        # print('corpus',corpus)
        return corpus

    # a1
    def scatter(self,x, colors):
        # We choose a color palette with seaborn.
        palette = np.array(sns.color_palette("hls", 10))

        # We create a scatter plot.
        f = plt.figure(figsize=(8, 8))
        ax = plt.subplot(aspect='equal')
        sc = ax.scatter(x[:, 0], x[:, 1], lw=0, s=40,
                        c=palette[colors])
        plt.xlim(-25, 25)
        plt.ylim(-25, 25)
        ax.axis('off')
        ax.axis('tight')

        # We add the labels for each digit.
        txts = []
        for i in range(10):
            # Position of each label.
            xtext, ytext = np.median(x[colors == i, :], axis=0)
            txt = ax.text(xtext, ytext, str(i), fontsize=24)
            txt.set_path_effects([
                PathEffects.Stroke(linewidth=5, foreground="w"),
                PathEffects.Normal()])
            txts.append(txt)

        return f, ax, sc, txts

    # a2
    def tsne(self):
        colors_list = ['red', 'blue', 'green', 'yellow', 'pink', 'gray', 'purple', 'orange']
        tsne = TSNE(n_components=2, init='pca', random_state=0)
        # result = tsne.fit_transform(self.weight)  # 进行数据降维
        # print(result)
        # self.scatter(result,colors_list)
        Y = tsne.fit_transform(self.weight)
        plt.scatter(Y[:, 0], Y[:, 0], c=colors_list, cmap=plt.cm.Special)
        plt.show()
        pass

    def kmeans_cluster(self):
        # self.clf = KMeans(n_clusters=8)
        # s = self.clf.fit(self.weight)
        # print(s)
        # print(self.clf.cluster_centers_)
        # print(self.clf.labels_)

        self.cluster = KMeans( init='k-means++', n_clusters=8)
        self.y_kmeans = self.cluster.fit(self.weight)  # 加载数据集合
        # ---- print(self.y_kmeans)
        r1 = pd.Series(self.cluster.labels_) # Series是一个一维的数据结构,labels是分的类别
        # print(r1)
        center_points = self.cluster.cluster_centers_
        # print(center_points)
        r2 = pd.DataFrame(self.cluster.cluster_centers_)
        # ---- print("聚类中心点", r2)
        # print(self.cluster.cluster_centers_)
        r = pd.concat([r2,r1],axis = 1)
        # r = pd.concat([pd.DataFrame(self.weight), pd.Series(self.cluster.labels_)], axis=1)
        # print(r)

        # --- print('各类别数目', pd.Series(self.cluster.labels_).value_counts())
        # print(self.cluster.labels_)
        print()
        # # 1-30 存储标签
        resNames = os.getcwd() + "/ingre_label_01-15-8-1.txt"
        result = open(resNames, 'a', encoding='utf-8')
        #
        # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        for i in range(len(self.weight)):
            result.write(str(r1[i]) + ' ')
            result.write('\n')

    def brich_cluster(self):
        print('start cluster Birch -------------------')
        self.cluster = Birch(threshold=0.6, n_clusters=None)
        self.cluster.fit_predict(self.weight)

    def get_title1(self):
        # self.cluster.labels_ 为聚类后corpus中文本index 对应 类别 {index: 类别} 类别值int值 相同值代表同一类
        cluster_dict = {}
        # cluster_dict key为Birch聚类后的每个类，value为 title对应的index
        for index, value in enumerate(self.cluster.labels_):
            if value not in cluster_dict:
                cluster_dict[value] = [index]
            else:
                cluster_dict[value].append(index)
        print(cluster_dict)
        print(sorted(cluster_dict.items(),key=lambda x:x[0]))
        print("-----before cluster Birch count title:", len(self.title_dict))
        # result_dict key为Birch聚类后距离中心点最近的title，value为sum_similar求和

        result_dict = {}
        for indexs in cluster_dict.values():
            latest_index = indexs[0]
            similar_num = len(indexs)
            if len(indexs) >= 2:
                min_s = np.sqrt(np.sum(np.square(
                    self.weight[indexs[0]] - self.cluster.subcluster_centers_[self.cluster.labels_[indexs[0]]])))
                for index in indexs:
                    s = np.sqrt(np.sum(
                        np.square(self.weight[index] - self.cluster.subcluster_centers_[self.cluster.labels_[index]])))
                    if s < min_s:
                        min_s = s
                        latest_index = index

            title = self.title_dict[latest_index]

            result_dict[title] = similar_num
        # print("-----after cluster Birch count title:", len(result_dict))
        for title in result_dict:
            print(title, result_dict[title])
        return result_dict

    def get_title(self):
        # self.cluster.labels_ 为聚类后corpus中文本index 对应 类别 {index: 类别} 类别值int值 相同值代表同一类

        # cluster_dict key为Birch聚类后的每个类，value为 title对应的index
        for index, value in enumerate(self.cluster.labels_):
            if value not in self.cluster_dict:
                self.cluster_dict[value] = [index]
            else:
                self.cluster_dict[value].append(index)
        # print(self.cluster_dict)
        # print(sorted(self.cluster_dict.items(),key=lambda x:x[0]))
        # print("-----before cluster Birch count title:", len(self.title_dict))
        # result_dict key为Birch聚类后距离中心点最近的title，value为sum_similar求和

    # 获取所有步骤列表
    def get_main_materials(self):
        with open(path_allData,'r',encoding='utf-8') as f_all:
            data = json.load(f_all)
            corpus = []  # 特征词，
            verb_words = []
            lists_m, lists_f, lists_g, lists_c = [], [], [], []
            index = 0
            all_steps = []
            for cate, info in data.items():
                for dish in info:
                    for pro, value in dish.items():
                        # if pro == '主料':
                        #     self.record_words(value, lists_m)
                        # if pro == '辅料':
                        #     self.record_words(value, lists_f)
                        # if pro == '配料':
                        #     self.record_words(value, lists_p)
                        # if pro == '厨具':
                        #     lists_c = self.record_words(value, lists_c)
                        # if pro == '工艺':
                        #     lists_g = self.record_words(value, lists_g)
                        if pro == '步骤':
                            # all_steps.append(value)
                            # print(1,value)
                            dish_steps = self.combine_step(value)

                    self.title_dict[index] = dish_steps
                    index = index + 1

                    c_words = self.cut_words(corpus, dish_steps, verb_words)


            self.get_cipin(c_words)
            self.kmeans_cluster()
            self.get_title()

            # get_verbs = self.combine_steps(all_steps)  # 获取所有步骤的动词
            # get_most_frequent = self.filter_words(get_verbs)  # 获取最高频动词

            # print(len(lists_m), lists_m)
            # print(len(lists_f), lists_f)
            # print(len(lists_p), lists_p)
            # self.combine_words(lists_m, lists_f, lists_p)

            # return lists_m, lists_f, lists_p

    def kmeans_vis(self):

        # with open(path_new_data,'r',encoding='utf-8') as f:
        #     data = json.load(f)
        #     index = 0
        #
        #     for line in data:
        #         if line['gid'] in clus_res[index][0]:
        #             res[index].append()
        #

        # 颜色和标签列表
        colors_list = ['red', 'blue', 'green','yellow','pink','gray','purple','orange']
        labels_list = ['Traditional','Normal','TA','Standard','Youth','b','c','d']

        # # 需要将DataFrame转成ndarray,才能进行 x[y_kmeans==i,0]
        x = self.weight

        for i in range(8):
            plt.scatter(x[self.y_kmeans==i,0], x[self.y_kmeans== i,1],c=colors_list[i],label=labels_list[i])
        # 聚类中心点
        plt.scatter(self.cluster.cluster_centers_[:,0],self.cluster.cluster_centers_[:,1], c='black',label='Centroids')

        plt.legend()
        plt.xlabel('Annual Income (k$)')
        plt.ylabel('Spending Score (1-100)')
        plt.show()

    def kmeans_evaluate(self):
        K = range(2, 12)
        meandistortions = []
        score = []
        for k in K:
            kmeans = KMeans(init='k-means++', n_clusters=k)
            kmeans.fit(self.weight)
            # print('center', kmeans.cluster_centers_)
            print('各类别数目', pd.Series(kmeans.labels_).value_counts())
            for index, value in enumerate(kmeans.labels_):
                if value not in self.cluster_dict:
                    self.cluster_dict[value] = [index]
                else:
                    self.cluster_dict[value].append(index)
            # print(self.cluster_dict)
            print(sorted(self.cluster_dict.items(), key=lambda x: x[0]))

            score.append(metrics.silhouette_score(self.weight, kmeans.labels_, metric='euclidean'))

            meandistortions.append(sum(np.min(cdist(self.weight, kmeans.cluster_centers_, 'euclidean'), axis=1)) / self.weight.shape[0])
        print('meandistortions',meandistortions)
        print('score',score)
        plt.plot(K, score, 'bx-')
        plt.xlabel('k')
        plt.ylabel(u'DEGREE')
        plt.show()
        pass

    def drawh(self):  # delimiter是数据分隔符
        outputfile = os.getcwd() + "/ingre_result_01-15-8-1.xlsx"
        # resName = os.getcwd() + "/0_mainclass_weight.txt"
        # resNames = os.getcwd() + "/0_maintype_label.txt"
        # resName = os.getcwd() + "/0_subclass_weight.txt"
        # resNames = os.getcwd() + "/0_subtype_label.txt"

        resName = os.getcwd() + "/ingre_weight_01-15-8-1.txt"
        resNames = os.getcwd() + "/ingre_label_01-15-8-1.txt"

        # # 1-28 读取文件并写入矩阵  权重
        fp = open(resName, 'r', encoding='utf-8')
        row_list = fp.readlines()  # splitlines默认参数是‘\n’
        fp.close()
        data_list = [[int(i) for i in row.strip().split(' ')] for row in row_list if
                     len(row[:-1].split('\r\n')[0]) > 0]
        res = np.mat(data_list)
        print(res)

        # 标签数据
        fpl = open(resNames, 'r', encoding='utf-8')
        row_list_label = fpl.readlines()  # splitlines默认参数是‘\n’
        # print(row_list_label)
        fpl.close()
        list_label = [int(row) for row in row_list_label]
        print("分类标签", list_label)

        colors_list = ['red', 'blue', 'green', 'yellow', 'pink', 'gray', 'purple', 'orange']
        tsne = TSNE(n_components=2)
        Y = tsne.fit_transform(res)  # 进行数据降维，fit_transform将X投影到一个嵌入空间并返回转换结果
        print("降维结果 ",Y)         #  Y 与 tsne.embedding_结果相同
        # C_Y = tsne.fit_transform(center_points)
        # print('center:', C_Y)
        r = pd.concat([pd.DataFrame(Y, columns=['x', 'y']), pd.Series(list_label)], axis=1)
        print("拼接降维结果与分类标签", r)
        r.to_excel(outputfile)

        # d = r[r[0] == 0]
        # plt.plot(d['x'], d['y'], 'r.')
        # d = r[r[0] == 1]
        # plt.plot(d['x'], d['y'], 'go')
        # d = r[r[0] == 2]
        # plt.plot(d['x'], d['y'], 'b*')
        # d = r[r[0] == 3]
        # plt.plot(d['x'], d['y'],color='gray')
        # d = r[r[0] == 4]
        # plt.plot(d['x'], d['y'], color='orange')
        # d = r[r[0] == 5]
        # plt.plot(d['x'], d['y'],color='green')
        # d = r[r[0] == 6]
        # plt.plot(d['x'], d['y'], color='yellow')
        # d = r[r[0] == 7]
        # plt.plot(d['x'], d['y'],color='pink')

        # d = r[r[0] == 1]
        # plt.plot(d['x'], d['y'], 'r.')
        # d = r[r[0] == 7]
        # plt.plot(d['x'], d['y'],'o', color = 'purple')
        # d = r[r[0] == 5]
        # plt.plot(d['x'], d['y'], 'b*')
        # d = r[r[0] == 3]
        # plt.plot(d['x'], d['y'],'o', color='gray')
        # d = r[r[0] == 4]
        # plt.plot(d['x'], d['y'],'o', color='orange')
        # d = r[r[0] == 6]
        # plt.plot(d['x'], d['y'],'o', color='green')
        # d = r[r[0] == 2]
        # plt.plot(d['x'], d['y'],'o', color='yellow')
        # d = r[r[0] == 0]
        # plt.plot(d['x'], d['y'],'o', color='pink')

        # plt.show()
        print('完成')

    # 获取所有主料列表
    def get_materials(self):
        with open(path_main_types,'r',encoding='utf-8') as f_all:
            data = json.load(f_all)
            corpus = []  # 特征词，
            lists_sub_class, lists_class, lists_g, lists_c = [], [], [], []
            for dish in data:
                for key,value in dish.items():
                    if key == 'subclass':
                        # self.get_matrixs(corpus, value)
                        # lists_sub_class = self.record_types(value, lists_sub_class)
                        t_words = self.get_matrixs(corpus, value)

            self.get_cipin(t_words)
            # self.tsne()
            self.kmeans_cluster()
            self.get_title()
            # self.kmeans_evaluate()

            # self.brich_cluster()
            # self.get_title()
            # print(len(lists_sub_class), lists_sub_class)
            # print(len(lists_p), lists_p)
            # self.combine_words(lists_m, lists_f, lists_p)

            # return lists_m, lists_f, lists_p



data = [[
      "煮熟牛肉丸和腊排骨。",
      "我用的土豆粉。",
      "热油放调料。",
      "炒香。",
      "加入水。",
      "煮开放土豆粉和腊排骨。",
      "拌一下。",
      "放入泡好的魔芋干和豆皮丝。",
      "然后放入其他配菜。",
      "煮几分钟放入适量盐和味精。",
      "捞出，热油放干辣椒炸一下淋上即可。",
      "最后撒上葱花。",
      "不错哦！"
    ],[
      "213煮熟牛肉丸和腊排骨。",
      "3我用的土豆粉。",
      "43热油放调料。",
      "炒香。",
      "5加入水。",
      "煮开放土豆粉和腊排骨。",
      "拌一下。",
      "放入泡好的魔芋干和豆皮丝。",
      "然后放入其他配菜。",
      "煮几分钟放入适量盐和味精。",
      "捞出，热油放干辣椒炸一下淋上即可。",
      "最后撒上葱花。",
      "不错哦！"
    ]]
res = []
if __name__ == '__main__':
    # hard_level()
    p = pre_cluster()


    # com = p.combine_steps(data)
    # p.filter_words(com)
    p.get_main_materials() # 步骤处理
    # p.get_materials()  # 食材处理
    # p.kmeans_evaluate()
    # p.hard_level()
    p.drawh()
    pass



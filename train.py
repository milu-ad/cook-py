import gensim,os,re

## 训练自己的词向量，并保存。
foods = os.getcwd() + "/food.txt"
# foodLists = []
# with open(foods,encoding='utf-8') as f1:
#     lines = f1.readlines()
#     for line in lines:
#         res = re.split('\t',line)
#         foodLists.append(res[0])
#     # print(foodLists)

def trainWord2Vec(filePath):

    sentences =  gensim.models.word2vec.LineSentence(filePath) # 读取分词后的 文本
    model = gensim.models.Word2Vec(sentences, size=50, window=5, min_count=1, workers=4) # 训练模型
    # sentences: 当然了，这是要训练的句子集，没有他就不用跑了
    # size: 这表示的是训练出的词向量会有几维
    # alpha: 机器学习中的学习率，这东西会逐渐收敛到 min_alpha
    # sg: 这个不是三言两语能说完的，sg = 1 表示采用skip - gram, sg = 0 表示采用cbow
    # window: 能往左往右看几个字的意思
    # workers: 执行绪数目，除非电脑不错，不然建议别超过
    # min_count: 若这个词出现的次数小于min_count，那他就不会被视为训练对象
    model.save('./Food_w2vec_50')


def testMyWord2Vec():
    # 读取自己的词向量，并简单测试一下 效果。
    inp = './Food_w2vec_50'  # 读取词向量
    model = gensim.models.Word2Vec.load(inp)

    # print('空间的词向量（50维）:',model['月宫饼'])
    print('打印最相近的5个词语：',model.wv.most_similar('土豆', topn=5))


if __name__ == '__main__':
    # trainWord2Vec(foods)
    testMyWord2Vec()
    pass
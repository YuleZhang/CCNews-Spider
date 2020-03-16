'''
@Author: YuleZhang
@Description: 
@Date: 2020-03-16 18:14:26
'''
# coding=utf-8
# 读取csv文件将评论合并进行聚类分析

import os
import pandas as pd
from numpy import *
import jieba
import re
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
import matplotlib as mpl

def readNews(df):
    # 将csv文档中content列合并为txt，防止字符串过长溢出
    # 若文件已存在则跳过
    if os.path.exists("newsContent.txt"):
        return
    df = pd.read_csv("test_data.csv",encoding='gbk')
    with open('newsContent.txt','a') as f:
        for index,row in df.iterrows():
            f.write(str(row['content'])+'\r\n')

def clean_news(text):
    # 去除数字
    l = list(filter(lambda x: x.isalpha(), text))
    t = ''.join(l)
    # 去除标点符号
    text = re.sub(r'[{}]+'.format('!,，;；:?'), '', t)
    return text.strip().lower()

def seg_word(sentence):
    """使用jieba对文档分词"""
    aft_clean = clean_news(sentence)
    seg_list = jieba.cut(aft_clean)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    # 读取停用词文件
    stopwords = set()
    fr = open('stopwords.txt', 'r',encoding='utf-8')
    for word in fr:
        stopwords.add(word.strip())
    fr.close()
    # 去除停用词
    return list(filter(lambda x: x not in stopwords, seg_result))


def read_from_file(file_name="newsContent.txt"):
    with open(file_name,"r") as fp:
        words = fp.read()
    return words

def stop_words(stop_word_file):
    words = read_from_file(stop_word_file)
    result = jieba.cut(words)
    new_words = []
    for r in result:
        new_words.append(r)
    return set(new_words)

def del_stop_words(words,stop_words_set):
#   words是已经切词但是没有去除停用词的文档。
#   返回的会是去除停用词后的文档
    result = jieba.cut(words)
    new_words = []
    for r in result:
        if r not in stop_words_set:
            new_words.append(r)
    return new_words

def get_all_vector(file_path,stop_words_set):
    names = [ os.path.join(file_path,f) for f in os.listdir(file_path) ]
    posts = [ open(name).read() for name in names ]
    docs = []
    word_set = set()
    for post in posts:
        doc = del_stop_words(post,stop_words_set)
        docs.append(doc)
        word_set |= set(doc)
        #print len(doc),len(word_set)

    word_set = list(word_set)
    docs_vsm = []
    #for word in word_set[:30]:
        #print word.encode("utf-8"),
    for doc in docs:
        temp_vector = []
        for word in word_set:
            temp_vector.append(doc.count(word) * 1.0)
        #print temp_vector[-30:-1]
        docs_vsm.append(temp_vector)

    docs_matrix = np.array(docs_vsm)

if __name__ == "__main__":
    df = pd.read_csv("test_data.csv", encoding='gbk')

    readNews(df)
    # 文档语料 空格连接
    corpus = []

    for index, row in df.iterrows():
        part = seg_word(str(row['content']))
        corpus.append(' '.join(part))
    # f = open('newsContent.txt','r')
    # lines = f.readlines()
    # cnt = 0
    # for line in lines:
    #     part = seg_word(line)
    #     for i in part:
    #         corpus.append(i)
    #     cnt+=1
    #     if cnt > 100:
    #        break
        # 参考: http://blog.csdn.net/abcjennifer/article/details/23615947
        # vectorizer = HashingVectorizer(n_features = 4000)
    # print(corpus)
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频

    vectorizer = CountVectorizer(max_features = 5000)

    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()

    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    print(weight.shape)
    # from sklearn.decomposition import PCA
    #

    # 打印特征向量文本内容
    print('Features length: ' + str(len(word)))

    clf = KMeans(n_clusters=2)
    s = clf.fit(weight)
    print(s)
    # 中心点
    print(clf.cluster_centers_)

    # 每个样本所属的簇
    label = []  # 存储1000个类标 3个类
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        # print(i, clf.labels_[i - 1])
        label.append(clf.labels_[i - 1])
        i = i + 1
    # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
    print('簇个数评估')
    print(clf.inertia_)

    # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
    pca = PCA(n_components=2)   # 保证降维后的数据保持80%的信息,whiten使得得到的数据进行归一化
    decomposition_data=pca.fit_transform(weight)   #训练降维后的数据，并进行标准化、归一化
    # tsne = TSNE(n_components=2)
    # decomposition_data = tsne.fit_transform(weight)
    print(decomposition_data.shape)
    # x = []
    # y = []

    # for i in decomposition_data:
    #     x.append(i[0])
    #     y.append(i[1])

    label_pred = clf.labels_ #获取聚类标签
    centroids = clf.cluster_centers_ #获取聚类中心
    inertia = clf.inertia_ # 获取聚类准则的总和
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    #这里'or'代表中的'o'代表画圈，'r'代表颜色为红色，后面的依次类推
    color = 0
    j = 0 
    for i in label_pred:
        plt.plot([decomposition_data[j:j+1,0]], [decomposition_data[j:j+1,1]], mark[i], markersize = 5)
        j +=1
    plt.savefig('./sample.png', aspect=1)

    # fig = plt.figure(figsize=(10, 10))
    # ax = plt.axes()
    # plt.scatter(x, y, c=clf.labels_, marker="x")
    # plt.xticks(())
    # plt.yticks(())

    # plt.savefig('./sample.png', aspect=1)
    #plt.show()


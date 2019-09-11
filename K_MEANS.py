# coding=utf-8 
import math
import time          
import re          
import os  
import sys
import codecs
import shutil
import numpy as np
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer

import Data

def GetDictHotSpot(list_datas, count, n):
    time_start = time.time()
    print("正在聚类...")

    #########################################################################
    #                           第一步 计算TFIDF

    #文档预料 空格连接
    corpus = []
    
    #读取预料 一行预料为一个文档
    for data in list_datas:
        corpus.append(data.content)
    
    print("开始处理...")
    #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
 
    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
 
    #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
 
    #获取词袋模型中的所有词语  
    word = vectorizer.get_feature_names()
 
    #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
 
    #打印特征向量文本内容
    print ('Features length: ' + str(len(word)))
    result = codecs.open("output/kmeans_tfidf.txt", 'w', 'utf-8')
    for j in range(len(word)):
        result.write(word[j] + ' ')
    result.write('\r\n\r\n')

    #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
    for i in range(len(weight)):
        #print (u"-------这里输出第",i,u"类文本的词语tf-idf权重------")  
        for j in range(len(word)):
            #print weight[i][j],
            result.write(str(weight[i][j]) + ' ')
        result.write('\r\n\r\n')

    result.close()
 
 
    ########################################################################
    #                               第二步 聚类Kmeans

    print ('Start Kmeans:')
    from sklearn.cluster import KMeans
    clf = KMeans(n_clusters = int( math.log(count) * 2 + n ), max_iter=300, n_init=40, init='k-means++',n_jobs=-1)
    s = clf.fit(weight)

    with open("output/kmeans_kmeans.txt", "w", encoding="utf-8") as file_kmeans:
        file_kmeans.write(str(s))
        file_kmeans.write("\n")
        #M个中心点
        file_kmeans.write(str(clf.cluster_centers_))
    
    #每个样本所属的簇
    with open("output/kmeans_i_cluster.txt", "w", encoding="utf-8") as file_result:
        file_result.write(str(clf.labels_))
        file_result.write("\n")
        i = 0
        while i < len(clf.labels_):
            file_result.write("%d : %d \n" % (i, clf.labels_[i]))
            i += 1
    
    dict_hotspot = {}
    index = 0
    while index < len(clf.labels_):
        # 文章下标 : index
        # 文章所属的簇 : clf.labels_[index]
        cluster = clf.labels_[index]
        if cluster not in dict_hotspot:
            dict_hotspot[cluster] = []
        dict_hotspot[cluster].append(list_datas[index])
        index += 1
    
    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print("评估值(越小越好) : %d / %d\n" % (clf.inertia_, len(list_datas)))

    with open("log", "a+", encoding="utf-8") as file_log:
        file_log.write("    %d\n" % clf.inertia_)

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))

    return dict_hotspot

def Output(dict_result, filename_result):
    with open(filename_result, "w", encoding="utf-8") as file_result:
        n = 1
        for key in dict_result.keys():
            if n > 1:
                file_result.write("\n")
            file_result.write("[ index = %3d ] [ Cluster = %d ] [ count = %d ]\n" % (n, key, len(dict_result[key])))
            count = 0
            for data in dict_result[key]:
                count += 1
                file_result.write(" %3d [ " % count)
                file_result.write(data.content)
                file_result.write(" ]\n")
            n += 1
 
if __name__ == "__main__":
    list_tweets = Data.GetListTweets("output/pretreatment_result.txt", 1000)
    dict_hotspot = GetDictHotSpot(list_tweets, 100)
    Output(dict_hotspot, "output/kmeans_hotspot.txt")

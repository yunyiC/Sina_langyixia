# coding=utf-8
import jieba
import numpy as np
from sklearn import feature_extraction    
from sklearn.feature_extraction.text import TfidfTransformer    
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import Birch

''' 
sklearn里面的TF-IDF主要用到了两个函数：CountVectorizer()和TfidfTransformer()。 
    CountVectorizer是通过fit_transform函数将文本中的词语转换为词频矩阵。 
    矩阵元素weight[i][j] 表示j词在第i个文本下的词频，即各个词语出现的次数。 
    通过get_feature_names()可看到所有文本的关键字，通过toarray()可看到词频矩阵的结果。 
    TfidfTransformer也有个fit_transform函数，它的作用是计算tf-idf值。 
'''

class Data:
    def __init__(self):
        self.ID = 0
        self.content = ''
        self.dict_words_tfidf = {}

    def toString(self):
        strR = '\
ID = %d\n\
content = %s\n\
words_tfidf = %s\n\
    '% (\
        self.ID, \
        self.content, \
        self.dict_words_tfidf)
        return strR

class Cluster():
    def load_datas(self, id_max = 0):
        print("加载数据...")
        datas = []
        with open("C_output_datas.txt", 'r', encoding='utf-8') as file_datas:
            list_in = file_datas.readlines()
            index = 0
            while index < len(list_in):
                if list_in[index].startswith("ID = "):
                    data = Data()
                    data.ID = int(list_in[index].replace("ID = ", ''))
                    data.content = list_in[index+2].replace("content_new = ", '').replace("\n", '')
                    data.dict_words_tfidf = eval(list_in[index+3].replace("words_tfidf = ", ''))
                    datas.append(data)
                    if id_max > 0 and data.ID >= id_max-1:
                        break
                index += 5
        return datas

    def init_data(self):
        print("初始化数据...")
        # corpus = [] #文档预料 空格连接
        corpus = []
        # f_write = open("jieba_result.dat","w")
        self.title_dict = {}

        datas = self.load_datas()
        index = 0
        for data in datas:
            line = data.content
            title = line.strip()
            self.title_dict[index] = title
            # seglist = jieba.cut(title,cut_all=False)#精确模式
            output = ' '.join(['%s'%x for x in list(data.dict_words_tfidf.keys())]).encode('utf-8')#空格拼接
            # print index,output
            index +=1
            corpus.append(output.strip())

        #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频  
        vectorizer = CountVectorizer()  
        #该类会统计每个词语的tf-idf权值  
        transformer = TfidfTransformer()  
        #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵  
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  
        #获取词袋模型中的所有词语    
        word = vectorizer.get_feature_names()
        #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重  
        self.weight = tfidf.toarray()
        # print self.weight

    def birch_cluster(self):
        print("处理数据...")
        print ('start cluster Birch -------------------' )
        self.cluster = Birch(threshold=0.6,n_clusters=None)
        self.cluster.fit_predict(self.weight)

        
    def get_title(self):
        print("保存数据...")
        # self.cluster.labels_ 为聚类后corpus中文本index 对应 类别 {index: 类别} 类别值int值 相同值代表同一类
        cluster_dict = {}
        # cluster_dict key为Birch聚类后的每个类，value为 title对应的index
        for index,value in enumerate(self.cluster.labels_):
            if value not in cluster_dict:
                cluster_dict[value] = [index]
            else:
                cluster_dict[value].append(index)
        with open("D_dict_cluster.txt", "w", encoding="utf-8") as file_cluster:
            for key,value in cluster_dict.items():
                file_cluster.write("%s : %s\n" % (str(key), str(value)))


        print ("-----before cluster Birch count title:",len(self.title_dict))
        # result_dict key为Birch聚类后距离中心点最近的title，value为sum_similar求和
        
        result_dict = {}
        for indexs in cluster_dict.values():
            latest_index = indexs[0]
            similar_num = len(indexs)
            if len(indexs)>=2:
                min_s = np.sqrt(np.sum(np.square(self.weight[indexs[0]]-self.cluster.subcluster_centers_[self.cluster.labels_[indexs[0]]])))
                for index in indexs:
                    s = np.sqrt(np.sum(np.square(self.weight[index]-self.cluster.subcluster_centers_[self.cluster.labels_[index]])))
                    if s<min_s:
                        min_s = s
                        latest_index = index

            title = self.title_dict[latest_index]

            result_dict[title] = similar_num
        
        print ("-----after cluster Birch count title : %d\n" % len(result_dict))
        with open("D_brich.txt", "w", encoding="utf-8") as file_brich:
            for title in result_dict:
                file_brich.write("(result:%d) %s\n" % (result_dict[title],title))
        
        
        datas = self.load_datas()
        with open("D_dict_result.txt", "w", encoding="utf-8") as file_cluster:
            count_max = 0
            index_max = 0
            for key,value in cluster_dict.items():
                file_cluster.write("%s : \n" % str(key))
                count = 0
                for index in value:
                    file_cluster.write("%s\n" % datas[index].content)
                    file_cluster.write("[ ")
                    for word in datas[index].dict_words_tfidf.keys():
                        file_cluster.write("%s " % word)
                    file_cluster.write("]\n")
                    count += 1
                if count > count_max:
                    count_max = count
                    index_max = key
                    
                file_cluster.write('\n')
            print("index_max = %d" % index_max)

        return result_dict
                    
    def run(self):
        self.init_data()
        self.birch_cluster()
        self.get_title()

if __name__=='__main__':
    cluster = Cluster()
    cluster.run()
    
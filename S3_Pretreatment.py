
import time
import re
import pynlpir
import math
import S1_Data

class Data_tweet:
    def __init__(self):
        self.ID = 0
        self.content_old = ''
        self.content = ''
        self.dict_words_tfidf = {}

    def toString(self):
        strR = '\
ID = %d\n\
content_old = %s\n\
content_new = %s\n\
words_tfidf = %s\n\
\n'% (\
        self.ID, \
        self.content_old, \
        self.content, \
        self.dict_words_tfidf)
        return strR


class Pretreatment:
    dict_words = {}
    dict_words_tf = {}

    def __init__(self):
        self.datas = []

    def deal(self, infos_tweet):
        time_start = time.time()
        print('处理数据中...')

        self.infos = infos_tweet

        self.noise_reduction()
        self.participle()
        self.filter()

        time_end = time.time()
        time_use = time_end - time_start
        print("用时 : " + str(time_use) + "s")
        
    def noise_reduction(self):
        #降噪
        print("正在降噪...")

        emojis = []
        with open("R2_emoji.txt", "r", encoding='utf-8') as file_emojis:
            for line in file_emojis:
                emoji = line.replace('\n', '')
                emojis.append(emoji)

        for info in self.infos:
            dataT = Data_tweet()
            dataT.ID = info.ID
            dataT.content_old = info.content
            contentT = dataT.content_old

            #去除微博内容中的微博表情，如[微笑]
            for emoji in emojis:
                if contentT.find(emoji) > -1:
                    contentT = contentT.replace(emoji, '')

            #去除微博内容中的网站地址，以http://开头
            filter_url = re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
            contentT = filter_url.sub('',contentT)
                
            #去除微博内容中的英文
            filter_english = re.compile(r'[a-zA-Z]+',re.S)
            contentT = filter_english.sub('', contentT)

            #去除@某某某
            contentT = re.sub('@([\u4E00-\u9FA5A-Za-z0-9_.-]+) ', '', contentT)

            #去除#
            contentT = contentT.replace('#', '')
            #去除空格
            contentT = contentT.replace(' ', '')
            
            dataT.content = contentT
            self.datas.append(dataT)

    def participle(self):
        #分词
        print("正在分词...")

        stopwords = []
        with open("R_stopwords.txt", "r", encoding="utf-8") as file_stopwords:
            for line in file_stopwords:
                stopword = line.replace('\n', '')
                stopwords.append(stopword)

        pynlpir.open()
        list_garbage = []
        for data in self.datas:
            try:
                # segments = pynlpir.segment(data.content, pos_names='all',pos_english=False)
                # file_nlp.write('\n')
                # for segment in segments:
                #     file_nlp.write("[ %s : %s ]" % (segment[0], segment[1]))
                #     file_nlp.write('\n')
                if len(data.content) < 8 :
                    raise RuntimeError("Error.len(content) < 5")
                key_words = pynlpir.get_key_words(data.content, max_words=70)
                if len(key_words) == 0 :
                    raise RuntimeError("Error.len(words) == 0")
                for word in key_words:
                    if word in stopwords:
                        continue
                    if word == '':
                        raise RuntimeError("Error.word = ''")
                    if word not in data.dict_words_tfidf:
                        contentT = data.content
                        count = 0
                        while contentT.find(word) > -1:
                            contentT = contentT.replace(word, '', 1)
                            count += 1
                        if count == 0 :
                            raise RuntimeError("Error.count == 0")
                        data.dict_words_tfidf[word] = count
                if len(data.dict_words_tfidf) == 0:
                    raise RuntimeError("Error.len(keys) == 0")
            except Exception as e:
                #数据无效,放入回收站
                data.e = str(e)
                list_garbage.append(data)
        #将数据从原始位置清除
        for data in list_garbage:
            self.datas.remove(data)
        with open("C_nlp_result.txt", "w", encoding='utf-8') as file_result:
            for data in self.datas:
                file_result.write(data.toString())
            #file_result.write('count.result = %d\n' % len(self.datas))
            print('有效结果 : %d' % len(self.datas))
        with open("C_nlp_garbage.txt", "w", encoding='utf-8') as file_garbage:
            for data in list_garbage:
                file_garbage.write("Error : %s\n" % data.e)
                file_garbage.write(data.toString())
            #file_garbage.write("count.garbage = %d\n" % len(list_garbage))
            print("无效结果 : %d" % len(list_garbage))
        pynlpir.close()

    def filter(self):
        #过滤
        #按照某个方向对不相关词汇进行删除
        print("正在过滤...")
        
        for data in self.datas:
            for word in data.dict_words_tfidf.keys():
                if word not in Pretreatment.dict_words:
                    Pretreatment.dict_words[word] = []
                    Pretreatment.dict_words_tf[word] = 0
                Pretreatment.dict_words[word].append(data)
                Pretreatment.dict_words_tf[word] = Pretreatment.dict_words_tf[word] + int(data.dict_words_tfidf[word])

        with open("C_dict_words.txt", 'w', encoding = 'utf-8') as file_dict_words:
            for keyWord in Pretreatment.dict_words:
                file_dict_words.write("Key : %s\n" % keyWord)
                file_dict_words.write("Tf : %d\n" % Pretreatment.dict_words_tf[keyWord])
                file_dict_words.write("Value : ")
                for valueData in Pretreatment.dict_words[keyWord]:
                    file_dict_words.write(" %d" % valueData.ID)
                file_dict_words.write('\n')
                file_dict_words.write('\n')

        for data in self.datas:
            count_tweet_all = 0
            for word in data.dict_words_tfidf.keys():
                count_tweet_all += data.dict_words_tfidf[word]
            for word in data.dict_words_tfidf.keys():
                data.dict_words_tfidf[word] = float(data.dict_words_tfidf[word]) / float(count_tweet_all)
                data.dict_words_tfidf[word] *= math.log(len(self.datas) / len(Pretreatment.dict_words[word]))

    def output(self):
        time_start = time.time()
        print("导出数据中...")

        with open("C_output_datas.txt", "w", encoding='utf-8') as file_output:
            for data in self.datas:
                file_output.writelines(data.toString())
            #file_output.writelines("count.data = %d" % len(self.datas))
            print("数据量 : %d" % len(self.datas))

        time_end = time.time()
        time_use = time_end - time_start
        print("用时 : " + str(time_use) + "s")

if __name__ == "__main__":
    #导入数据
    # info_information = S1_Data.loadInformation()
    # info_relationship = S1_Data.loadRelationship()
    info_tweet = S1_Data.loadTweet()
    
    #处理数据
    pretreatment = Pretreatment()
    pretreatment.deal(info_tweet)

    #导出数据
    pretreatment.output()
    
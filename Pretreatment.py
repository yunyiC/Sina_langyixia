
import time
import re
import pynlpir
import math
import Data


def GetListWords(filename):
    list_words = []
    with open(filename, "r", encoding='utf-8') as file_words:
        for line in file_words:
            word = line.replace('\n', '')
            list_words.append(word)
    return list_words

def NoiseReduction(list_datas, filename_words_sensitive, filename_words_emoji):
    #降噪
    time_start = time.time()
    print("正在降噪...")

    list_garbagesT.clear()
    list_words_sensitive = GetListWords(filename_words_sensitive)
    list_words_emoji = GetListWords(filename_words_emoji)


    for data in list_datas:
        data.content_old = data.content
        contentT = data.content

        #如果包含敏感词,直接舍弃
        isGarbage = False
        for word in list_words_sensitive:
            if contentT.find(word) > -1:
                data.error = "包含敏感词"
                isGarbage = True
                break
        
        if (data.comment + data.like + data.transfer) <= 10:
            data.error = "评论数太少"
            isGarbage = True

        if isGarbage:
            list_garbagesT.append(data)
            continue

        #去除微博内容中的微博表情，如[微笑]
        for word in list_words_emoji:
            if contentT.find(word) > -1:
                contentT = contentT.replace(word, '')

        #去除微博内容中的]
        filter_english = re.compile(r'([\u4e00-\u9fa5]+)]',re.S)
        contentT = filter_english.sub('', contentT)

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
        #去除[
        contentT = contentT.replace('[', '')
        #去除]
        contentT = contentT.replace(']', '')
        
        data.content = contentT
    
    for data in list_garbagesT:
        list_datas.remove(data)
        list_garbages.append(data)
    list_garbagesT.clear()
    
    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_datas


def Participle(list_datas, filename_stopwords):
    #分词
    time_start = time.time()
    print("正在分词...")

    list_garbagesT.clear()
    list_words_stop = GetListWords(filename_stopwords)

    pynlpir.open()
    for data in list_datas:
        # segments = pynlpir.segment(data.content, pos_names='all',pos_english=False)
        # file_nlp.write('\n')
        # for segment in segments:
        #     file_nlp.write("[ %s : %s ]" % (segment[0], segment[1]))
        #     file_nlp.write('\n')
        
        if len(data.content) < 8 :
            data.error = "内容过短"
            list_garbagesT.append(data)
            continue
        list_words = pynlpir.get_key_words(data.content, max_words=70)
        if len(list_words) == 0 :
            data.error = "没有分词结果"
            list_garbagesT.append(data)
            continue
        #print("开始停词")
        for word in list_words:
            if word in list_words_stop:
                #print("停了个词" + word)
                continue
            if word == '':
                data.error = "包含空白分词"
                list_garbagesT.append(data)
                break
            #统计词频
            contentT = data.content
            count = 0
            while contentT.find(word) > -1:
                contentT = contentT.replace(word, '', 1)
                count += 1
            if count == 0 :
                data.error = "分词不属于原文"
                list_garbagesT.append(data)
                break
            #保存词频统计结果
            data.dict_words_tfidf[word] = count
        if len(data.dict_words_tfidf) == 0:
            data.error = "词频统计结果为空"
            list_garbagesT.append(data)
            continue
    
    #清除垃圾数据
    for data in list_garbagesT:
        list_datas.remove(data)
        list_garbages.append(data)
    list_garbagesT.clear()

    pynlpir.close()

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_datas

def Filter(list_datas):
    #过滤
    #按照某个方向对不相关词汇进行删除
    time_start = time.time()
    print("正在过滤...")

    list_garbagesT.clear()
    
    for data in list_datas:
        for word in data.dict_words_tfidf.keys():
            if word not in dict_words_data:
                dict_words_data[word] = []
                dict_words_tf[word] = 0
            dict_words_data[word].append(data)
            dict_words_tf[word] = dict_words_tf[word] + int(data.dict_words_tfidf[word])

    for data in list_datas:
        count_tweet_all = 0
        for word in data.dict_words_tfidf.keys():
            count_tweet_all += data.dict_words_tfidf[word]
        for word in data.dict_words_tfidf.keys():
            data.dict_words_tfidf[word] = float(data.dict_words_tfidf[word]) / float(count_tweet_all)
            data.dict_words_tfidf[word] *= math.log(len(list_datas) / len(dict_words_data[word]))

    #清除垃圾数据
    for data in list_garbagesT:
        list_datas.remove(data)
        list_garbages.append(data)
    list_garbagesT.clear()

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_datas

def OutputDictWords(filename_dictwords):
    time_start = time.time()
    print("导出词频统计结果中...")

    with open(filename_dictwords, 'w', encoding = 'utf-8') as file_output:
        for word in dict_words_data:
            file_output.write("Key : [ %s ]\n" % word)
            file_output.write("Tf : [ %d ]\n" % dict_words_tf[word])
            file_output.write("Value : ")
            for data in dict_words_data[word]:
                file_output.write("%d " % data.ID)
            file_output.write(' \n\n')
    
    print("数据量 : %d" % len(dict_words_data))

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))

def OutputGarbages(filename_garbages):
    time_start = time.time()
    print("导出弃用数据中...")

    with open(filename_garbages, 'w', encoding = 'utf-8') as file_output:
        for data in list_garbages:
            file_output.write(data.ToString())
            file_output.write("\n")

    print("数据量 : %d" % len(list_garbages))
    
    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))

def Pretreatment(list_tweets, filename_words_sensitive, filename_words_emoji, filename_stopwords):
    time_start = time.time()
    print("预处理...")

    list_datas = list_tweets
    list_datas = NoiseReduction(list_datas, filename_words_sensitive, filename_words_emoji)
    list_datas = Participle(list_datas, filename_stopwords)
    list_datas = Filter(list_datas)

    time_end = time.time()
    print("预处理用时 : %.2f s" % (time_end - time_start))

    return list_datas

dict_words_data = {}
dict_words_tf = {}
list_garbages = []
list_garbagesT = []

if __name__ == "__main__":
    list_tweets = Data.GetListTweets("output/datas_tweets.txt", 5000)
    list_result = Pretreatment(list_tweets, "input/sensitive.txt", "input/emoji.txt", "input/stopwords.txt")
    Data.OutputToFile(list_result, "output/pretreatment_result.txt")
    OutputDictWords("output/pretreatment_dictwords.txt")
    OutputGarbages("output/pretreatment_garbages.txt")
    
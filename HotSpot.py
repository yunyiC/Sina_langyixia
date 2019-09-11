import datetime

class HotSpot:
    def __init__(self):
        self.cluster = 0
        self.datas = None
        self.value = 0
        self.index = 0
        self.count = 0
        self.dict_hotWords = {}

def GetTf(content, word):
    if word == '':
        return 1
    if content.find(word) == -1:
        return 1
    tf = 0
    while content.find(word) > -1:
        tf += 1
        if tf > 1000:
            print("词频超标 : content = %s , word = %s \n" % (content, word))
            break
        content = content.replace(word, '', 1)
    return tf

def GetListHotSpot(dict_hotSpot):

    print("统计话题的热度值...")
    list_hotSpot = []
    for cluster in dict_hotSpot.keys():
        if len(dict_hotSpot[cluster]) < 6:
            # 推文数量较少,不作为热点
            continue
        hotSpot = HotSpot()
        hotSpot.cluster = cluster
        hotSpot.datas = dict_hotSpot[cluster]
        for data in hotSpot.datas:
            hotSpot.value += data.comment
            hotSpot.value += data.like
            hotSpot.value += data.transfer
        list_hotSpot.append(hotSpot)
    
    list_hotSpot_sorted  = sorted(list_hotSpot, key=lambda hotSpot : hotSpot.value, reverse=True)

    print("统计热词...")

    index = 0
    for hotSpot in list_hotSpot_sorted:
        index += 1
        hotSpot.index = index
        hotSpot.count = len(hotSpot.datas)
        dict_Ei = {}
        dict_Tf = {}
        for data in hotSpot.datas:
            for word in data.dict_words_tfidf.keys():
                if word not in hotSpot.dict_hotWords:
                    hotSpot.dict_hotWords[word] = 0.0
                    dict_Ei[word] = 0
                    dict_Tf[word] = 0
                dict_Ei[word] += 1
                dict_Tf[word] += GetTf(data.content, word)
        
        for word in hotSpot.dict_hotWords.keys():
            hotSpot.dict_hotWords[word] = dict_Ei[word] * dict_Tf[word]
        hotSpot.list_hotWords = sorted(hotSpot.dict_hotWords, key=lambda word: hotSpot.dict_hotWords[word], reverse=True)

    return list_hotSpot_sorted

def Output(list_hotSpot, filename):
    print("存储热点...")
    with open(filename, "w", encoding="utf-8") as file_result:
        index = 0
        for hotSpot in list_hotSpot:
            index += 1
            file_result.write("[ index = %d ]\n" % hotSpot.index)
            file_result.write("[ cluster = %d ]\n" % hotSpot.cluster)
            file_result.write("[ count = %d ]\n" % hotSpot.count)
            file_result.write("[ value = %d ]\n" % hotSpot.value)
            file_result.write("[ hot_words = ")
            count = 0
            for word in hotSpot.list_hotWords:
                count += 1
                if (count > 10):
                    break
                file_result.write("%s(%d) " % (word, int(hotSpot.dict_hotWords[word])))
            file_result.write("]\n")
            file_result.write("[ index ] [ ID ] [ comment ] [ like ] [ transfer ] [ content ]\n")
            count = 0
            for data in hotSpot.datas:
                count += 1
                file_result.write("[ %3d ] [ %6d ] [ %6d ] [ %6d ] [ %6d ] [ %s ]\n" \
                                 % (count, data.ID, data.comment, data.like, data.transfer, data.content))
                
            file_result.write("\n")
        print("共 %d 个热点\n" % index)


def Date_interval_list(date_start = None,date_end = None):
	if date_start is None:
		date_start = '2019-07-01'
	if date_end is None:
		date_end = datetime.datetime.now().strftime('%Y-%m-%d')
 
	date_start=datetime.datetime.strptime(date_start,'%Y-%m-%d')
	date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
	date_list = []
	date_list.append(date_start.strftime('%Y-%m-%d'))
	while date_start < date_end:
	    date_start+=datetime.timedelta(days=+1)# 日期加一天
	    date_list.append(date_start.strftime('%Y-%m-%d'))# 日期存入列表
	return date_list

def Select_date(date_start = None,date_end = None):
    date_list = []
    if date_start is None:
	    date_start = '2019-07-01'
    if date_end is None:
	    date_end = datetime.datetime.now().strftime('%Y-%m-%d')
    date_list = Date_interval_list(date_start,date_end)
    file_list = []
    for date in date_list:
        filename = "date/" + str(date) + ".txt"
        file_list.append(filename)
    return file_list
    

import Data
import K_MEANS
import Pretreatment

if __name__ == "__main__":
    list_tweets = []
    #list_tweets = Data.GetListTweets("output/datas_tweets.txt", 5000)
    date_start = '2019-09-05'
    date_end = '2019-09-06'
    n = 10  #决定聚类数量
    pretreatment_result = "output/" + date_start + "_" + date_end + "_" + "pretreatment_result" + ".txt"
    hotspot_result = "output/" + date_start + "_" + date_end + "_" + "hotspot_result" + ".txt"

    # #实验获取手肘值
    # for f in Select_date(date_start,date_end):
    #     list_tweets.extend(Data.GetListTweets(f))
    # list_result = Pretreatment.Pretreatment(list_tweets, "input/sensitive.txt", "input/emoji.txt", "input/stopwords.txt")
    # count = Data.OutputToFile(list_result, pretreatment_result)
    
    # list_tweets = Data.GetListTweets(pretreatment_result)
        
    

    for f in Select_date(date_start,date_end):
        list_tweets.extend(Data.GetListTweets(f))
    
    list_result = Pretreatment.Pretreatment(list_tweets, "input/sensitive.txt", "input/emoji.txt", "input/stopwords.txt")
    count = Data.OutputToFile(list_result, pretreatment_result)
    
    list_tweets = Data.GetListTweets(pretreatment_result)
    dict_hotSpot = K_MEANS.GetDictHotSpot(list_tweets,count,n)
    list_hotSpot = GetListHotSpot(dict_hotSpot)
    
    Output(list_hotSpot, hotspot_result)

  
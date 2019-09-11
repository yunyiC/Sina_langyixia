import os
import time

'''
Tweet{
_id=3164835813-M_EDaey5egI, 
Comment=999, 
Content=如果你越来越肥 证明了 身边有个人宠你 ​​​, 
ID=3164835813, 
Like=1312, 
PubTime=04月06日 01:08, 
Transfer=637

Co_oridinates=39.70168,118.24656
Tools=微博 weibo.com
}
'''

class Tweet:
    id_now = -1
    @classmethod
    def GetID(cls):
        cls.id_now = cls.id_now + 1
        return cls.id_now

    def __init__(self):
        self.ID = Tweet.GetID()
        self.content = ''
        self.content_old = ''
        self.comment = 0
        self.like = 0
        self.transfer = 0
        self.year = 0
        self.month = 0
        self.day = 0
        self.value = 0
        self.dict_words_tfidf = {}
        self.error = ''
        self.id_author = 0
        self.id_hotspot = 0

    def ToString(self):
        strR = '\
ID = [ %d ]\n\
Content = [ %s ]\n\
Content(old) = [ %s ]\n\
Comment = [ %d ]\n\
Like = [ %d ]\n\
Transfer = [ %d ]\n\
year = [ %d ]\n\
month = [ %d ]\n\
day = [ %d ]\n\
value = [ %d ]\n\
dict_words_tfidf = [ %s ]\n\
error = [ %s ]\n\
ID(author) = [ %d ]\n\
ID(hotspot) = [ %d ]\n\
' % (\
        self.ID, \
        self.content, \
        self.content_old, \
        self.comment, \
        self.like, \
        self.transfer, \
        self.year, \
        self.month, \
        self.day, \
        self.value, \
        str(self.dict_words_tfidf), \
        self.error, \
        self.id_author, \
        self.id_hotspot)

        return strR


'''
Relationship{
_id=58e7176c57fc6b17e4b87328, 
Host1=5886607128, 
Host2=5669038139
}
'''

class Relationship:
    id_now = -1
    @classmethod
    def GetID(cls):
        cls.id_now = cls.id_now + 1
        return cls.id_now

    def __init__(self):
        self.ID = Relationship.GetID()
        self._id = 0
        self.host1 = 0
        self.host2 = 0

    def ToString(self):
        strR = '\
ID = [ %d ]\n\
_id = [ %d ]\n\
host1 = [ %d ]\n\
host2 = [ %d ]\n\
' % (\
        self.ID, \
        self._id, \
        self.host1, \
        self.host2)
        return strR


'''
Infomation{
_id=2354184981, 
Num_Follows=555, 
City=广州, 
Num_Tweets=1118, 
AvatarLink=http://tva3.sinaimg.cn/crop.0.0.750.750.180/8c520315jw8fb9b3jv2n1j20ku0kuq3m.jpg, 
Province=广东, 
URL=http://weibo.com/u/2354184981, 
Gender=女, 
Num_Fans=616, 
Birthday=Tue Nov 24 00:00:00 CST 1992, 
InsertTime=2017-04-07 12:36:18, 
avatar_saved=1, 
VIPlevel=4级, 
NickName=静宜菌爱煮鸡, 
BriefIntroduction=一枚小吃货。。简单快乐着。。
}
'''

class Information:
    id_now = -1
    @classmethod
    def GetID(cls):
        cls.id_now = cls.id_now + 1
        return cls.id_now

    def __init__(self):
        self.ID = Information.GetID()
        self._id = 0
        self.num_Follows = 0
        self.city = ''
        self.num_Tweets = 0
        self.avatarLink = ''
        self.province = ''
        self.url = ''
        self.gender = ''
        self.num_Fans = 0
        self.birthday = ''
        self.insertTime = ''
        self.avatar_saved = 0
        self.viplevel = ''
        self.nickName = ''
        self.briefIntroduction = ''

    def ToString(self):
        strR = '\
ID = [ %d ]\n\
_id = [ %d ]\n\
Num_Follows = [ %d ]\n\
City = [ %s ]\n\
Num_Tweets = [ %d ]\n\
AvatarLink = [ %s ]\n\
Province = [ %s ]\n\
URL = [ %s ]\n\
Gender = [ %s ]\n\
Num_Fans = [ %d ]\n\
Birthday = [ %s ]\n\
InsertTime = [ %s ]\n\
avatar_saved = [ %d ]\n\
VIPLevel = [ %s ]\n\
NickName = [ %s ]\n\
BriefIntroduction = [ %s ]\n'  \
                % (\
                self.ID,  \
                self._id,  \
                self.num_Follows,  \
                self.city,  \
                self.num_Tweets,  \
                self.avatarLink,  \
                self.province,  \
                self.url,  \
                self.gender,  \
                self.num_Fans,  \
                self.birthday,  \
                self.insertTime,  \
                self.avatar_saved,  \
                self.viplevel,  \
                self.nickName,  \
                self.briefIntroduction)
        return strR

##################################################################################

def GetListRelationshipsFromJson(filename, count_max=0):
    time_start = time.time()
    print("读取 %s 中..." % filename)
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    list_relationships = []
    with open(filename, encoding='utf-8') as file_relationship:
        count = 0
        for line_relationship in file_relationship:
            count += 1
            if count_max > 0 and count > count_max:
                break
            if not line_relationship.startswith('{'):
                print("错误: 行:%d 内容:%s" % (count, line_relationship))
            else:
                #去掉前后的大括号
                line_relationship = line_relationship.replace('{', '')
                line_relationship = line_relationship.replace('}\n', '')
                column_relationship = line_relationship.split(', ')
                relationship = Relationship()
                for columnT in column_relationship:
                    #print(columnT)
                    if columnT.startswith('_id='):
                        relationship._id = columnT[columnT.find('=')+1:]
                        relationship._id = int(relationship._id, 16)
                    elif columnT.startswith('Host1='):
                        relationship.host1 = columnT[columnT.find('=')+1:]
                        relationship.host1 = int(relationship.host1)
                    elif columnT.startswith('Host2='):
                        relationship.host2 = columnT[columnT.find('=')+1:]
                        relationship.host2 = int(relationship.host2)
                    else:
                        print('未知: ' + columnT)
                list_relationships.append(relationship)

    print("数据量 : %d" % len(list_relationships))

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_relationships


def GetListTweetsFromJson(filename, count_max=0):
    time_start = time.time()
    print("读取 %s 中..." % filename)
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    list_tweets = []
    with open(filename, encoding='utf-8') as file_tweets:
        count = 0
        for line_tweet in file_tweets:
            count = count + 1
            if count_max > 0 and count > count_max:
                break
            if not line_tweet.startswith('{'):
                print("错误: 行:%d 内容:%s " % (count, line_tweet))
            else:
                #创建一个对象
                tweet = Tweet()
                #去掉前后的大括号
                line_tweet = line_tweet.replace('{', '')
                line_tweet = line_tweet.replace('}\n', '')
                #先排除content对后续断句的干扰
                strT_Content = ', Content='
                strT_ID = ', ID='
                indexT_Content = line_tweet.find(strT_Content)
                indexT_ID = line_tweet.find(strT_ID)
                tweet.content = line_tweet[indexT_Content + len(strT_Content):indexT_ID]
                line_tweet = line_tweet[:indexT_Content] + line_tweet[indexT_ID:]
                
                #正常断句
                #用逗号分成子字符串
                try:
                    column_tweet = line_tweet.split(', ')
                    for columnT in column_tweet:
                        #print(columnT)
                        if columnT.startswith('_id='):
                            _id = columnT[columnT.find('=')+1:]
                        elif columnT.startswith('Comment='):
                            tweet.comment = columnT[columnT.find('=')+1:]
                            tweet.comment = int(float(tweet.comment))
                        elif columnT.startswith('ID='):
                            tweet.id_author = columnT[columnT.find('=')+1:]
                            tweet.id_author = int(tweet.id_author)
                        elif columnT.startswith('Like='):
                            tweet.like = columnT[columnT.find('=')+1:]
                            tweet.like = int(float(tweet.like))
                        elif columnT.startswith('PubTime='):
                            pubTime = columnT[columnT.find('=')+1:]
                        elif columnT.startswith('Transfer='):
                            tweet.transfer = columnT[columnT.find('=')+1:]
                            tweet.transfer = int(float(tweet.transfer))
                        elif columnT.startswith('Co_oridinates='):
                            co_oridinates = columnT[columnT.find('=')+1:]
                        elif columnT.startswith('Tools='):
                            tools = columnT[columnT.find('=')+1:]
                        else:
                            print("未知: " + columnT)
                    str_date = pubTime
                    if str_date.find('-') > -1:
                        str_date = str_date[:str_date.find(' ')]
                        str_date = str_date.split('-')
                        tweet.year = int(str_date[0])
                        tweet.month = int(str_date[1])
                        tweet.day = int(str_date[2])
                    elif str_date.find('月') > -1:
                        tweet.year = 2017
                        tweet.month = int(str_date[:str_date.find('月')])
                        tweet.day = int(str_date[str_date.find('月')+1:str_date.find('日')])
                    elif str_date.find('今天') > -1:
                        tweet.year = 2017
                        tweet.month = 4
                        tweet.day = 20
                    elif str_date.find('分钟前') > -1:
                        tweet.year = 2017
                        tweet.month = 4
                        tweet.day = 20
                    
                    list_tweets.append(tweet)
                except Exception as e:
                    print (e)
                    print ("line = %d" % count)

    print("数据量 : %d" % len(list_tweets))

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_tweets


def GetListInformationsFromJson(filename, count_max=0):
    time_start = time.time()
    print("读取 %s 中..." % filename)
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    info_information = []
    with open(filename, encoding='utf-8') as file_informations:
        id_line = 0
        for line_information in file_informations:
            id_line = id_line + 1
            if count_max > 0 and id_line > count_max:
                break
            if not line_information.startswith('{'):
                print("错误: 行:%d 内容: %s" % (id_line, line_information))
            else:
                #创建一个对象
                information = Information()
                #去掉前后的大括号
                line_information = line_information.replace('{', '')
                line_information = line_information.replace('}\n', '')
                
                #排除BriefIntroduction的影响
                strT_BriefIntroduction = ', BriefIntroduction='
                indexT_BriefIntroduction = line_information.find(strT_BriefIntroduction)
                if indexT_BriefIntroduction > 0:
                    information.briefIntroduction = line_information[indexT_BriefIntroduction + len(strT_BriefIntroduction):]
                    line_information = line_information[:indexT_BriefIntroduction]

                #排除URL的影响
                #, URL=从业者, 从事互联网产品设计和策划、网站运营等工作。关注医院平台网络营销。】现担任北京巨龙副总。, Gender=男
                strT_URL = ', URL='
                indexT_URL = line_information.find(strT_URL)
                strT_Gender = ', Gender='
                indexT_Gender = line_information.find(strT_Gender)
                information.url = line_information[indexT_URL + len(strT_URL):indexT_Gender]
                line_information = line_information[:indexT_URL] + line_information[indexT_Gender:]

                #用逗号分成子字符串
                column_information = line_information.split(', ')
                for columnT in column_information:
                    #print(columnT)
                    if columnT.startswith('_id='):
                        information._id = columnT[columnT.find('=')+1:]
                        information._id = int(information._id)
                    elif columnT.startswith('Num_Follows='):
                        information.num_Follows = columnT[columnT.find('=')+1:]
                        information.num_Follows = int(float(information.num_Follows))
                    elif columnT.startswith('City='):
                        information.city = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Num_Tweets='):
                        information.num_Tweets = columnT[columnT.find('=')+1:]
                        information.num_Tweets = int(float(information.num_Tweets))
                    elif columnT.startswith('AvatarLink='):
                        information.avatarLink = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Province='):
                        information.province = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Gender='):
                        information.gender = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Num_Fans='):
                        information.num_Fans = columnT[columnT.find('=')+1:]
                        information.num_Fans = int(float(information.num_Fans))
                    elif columnT.startswith('Birthday='):
                        information.birthday = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('InsertTime='):
                        information.insertTime = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('avatar_saved='):
                        information.avatar_saved = columnT[columnT.find('=')+1:]
                        information.avatar_saved = int(information.avatar_saved)
                    elif columnT.startswith('VIPlevel='):
                        information.viplevel = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('NickName='):
                        information.nickName = columnT[columnT.find('=')+1:]
                    else:
                        print("未知: " + columnT)
                info_information.append(information)
    
    print("数据量 : %d" % len(info_information))

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return info_information

##########################################################################################

def GetListTweets(filename, count_max=0):
    time_start = time.time()
    print(" %s 读取中..." % filename)
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    list_tweets = []

    if os.path.exists(filename):
        pass
    else:
        return  list_tweets
    
    count = 0
    with open(filename, "r", encoding='utf-8') as file_tweets:
        tweet = Tweet()
        for line in file_tweets:
            if line.startswith("ID = [ "):
                tweet.ID = int(line[line.find('[')+2:-2])
                # print("ID = %d" % tweet.ID)
            elif line.startswith("Content = [ "):
                tweet.content = line[line.find('[')+2:-2]
            elif line.startswith("Content(old) = [ "):
                tweet.content_old = line[line.find('[')+2:-2]
            elif line.startswith("Comment = [ "):
                tweet.comment = int(line[line.find('[')+2:-2])
            elif line.startswith("Like = [ "):
                tweet.like = int(line[line.find('[')+2:-2])
            elif line.startswith("Transfer = [ "):
                tweet.transfer = int(line[line.find('[')+2:-2])
            elif line.startswith("year = [ "):
                tweet.year = int(line[line.find('[')+2:-2])
            elif line.startswith("month = [ "):
                tweet.month = int(line[line.find('[')+2:-2])
            elif line.startswith("day = [ "):
                tweet.day = int(line[line.find('[')+2:-2])
            elif line.startswith("value = [ "):
                tweet.value = int(line[line.find('[')+2:-2])
            elif line.startswith("dict_words_tfidf = [ "):
                tweet.dict_words_tfidf = eval(line[line.find('[')+2:-2])
            elif line.startswith("error = [ "):
                tweet.error = line[line.find('[')+2:-2]
            elif line.startswith("ID(author) = [ "):
                tweet.id_author = int(line[line.find('[')+2:-2])
            elif line.startswith("ID(hotspot) = [ "):
                tweet.id_hotspot = int(line[line.find('[')+2:-2])
            else:
                list_tweets.append(tweet)
                count += 1
                if count_max != 0 and count == count_max:
                    break
                tweet = Tweet()

    print("数据量 : %d" % len(list_tweets))

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_tweets


def GetListRelationships(filename, count_max=0):
    time_start = time.time()
    print(" %s 读取中..." % filename)
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    list_relationships = []
    
    count = 0
    with open(filename, encoding='utf-8') as file_relationships:
        relationship = Relationship()
        for line in file_relationships:
            if line.startswith("ID = [ "):
                relationship.ID = int(line[line.find('[')+2:-2])
            elif line.startswith("_id = [ "):
                relationship._id = int(line[line.find('[')+2:-2])
            elif line.startswith("host1 = [ "):
                relationship.host1 = int(line[line.find('[')+2:-2])
            elif line.startswith("host2 = [ "):
                relationship.host2 = int(line[line.find('[')+2:-2])
            else:
                list_relationships.append(relationship)
                count += 1
                if count == count_max:
                    break
                relationship = Relationship()

    print("数据量 : %d" % len(list_relationships))

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return list_relationships


##########################################################################################

def OutputToFile(list_datas, filename):
    #导出数据
    time_start = time.time()
    print("导出数据中...")
    with open(filename, 'w', encoding='utf-8') as file_output:
        count = 0
        for data in list_datas:
            count += 1
            if count > 1:
                file_output.write('\n')
            file_output.write(data.ToString())
    
    print("数据量 : %d" % count)

    time_end = time.time()
    print("用时 : %.2f s" % (time_end - time_start))
    return count

def GetData(list_datas, ID):
    left = 0
    right = len(list_datas)-1
    if not left < right:
        return None
    if list_datas[right].ID == ID:
        return list_datas[right]
    while left < right:
        middle = (left + right) / 2
        middle = int(middle)
        if list_datas[middle].ID == ID:
            return list_datas[middle]
        elif list_datas[middle].ID > ID:
            right = middle
        else:
            left = middle
    return None


if __name__ == "__main__":
    # list_tweets = GetListTweetsFromJson("input/Tweets.json")
    # OutputToFile(list_tweets, "output/datas_tweets.txt")

    list_tweets = GetListTweets("output/datas_tweets.txt", 100)
    data = GetData(list_tweets, 59)
    print(data.ToString())
    data = GetData(list_tweets, 0)
    print(data.ToString())
    data = GetData(list_tweets, 99)
    print(data.ToString())

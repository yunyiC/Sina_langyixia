
import time

def loadRelationship(count_max=0):
    time_start = time.time()
    print("读取 Relationship 文件中...")
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    
    info_relationship = []
    with open("R_Relationships.json", encoding='utf-8') as file_relationship:
        list_relationship = file_relationship.readlines()
        id_line = 0
        for line_relationship in list_relationship:
            id_line = id_line + 1
            if count_max > 0 and id_line > count_max:
                break
            if not line_relationship.startswith('{'):
                print("错误: 行:%d 内容:%s" % (id_line, line_relationship))
            else:
                #去掉前后的大括号
                line_relationship = line_relationship.replace('{', '')
                line_relationship = line_relationship.replace('}\n', '')
                column_relationship = line_relationship.split(', ')
                info_current = Relationship()
                for columnT in column_relationship:
                    #print(columnT)
                    if columnT.startswith('_id='):
                        info_current._id = columnT[columnT.find('=')+1:]
                        info_current._id = int(info_current._id, 16)
                    elif columnT.startswith('Host1='):
                        info_current.host1 = columnT[columnT.find('=')+1:]
                        info_current.host1 = int(info_current.host1)
                    elif columnT.startswith('Host2='):
                        info_current.host2 = columnT[columnT.find('=')+1:]
                        info_current.host2 = int(info_current.host2)
                    else:
                        print('未知: ' + columnT)
                info_relationship.append(info_current)

    count = len(info_relationship)
    print("数据量 : %d" % count)
    time_end = time.time()
    time_use =  time_end - time_start
    print("用时 : " + str(time_use) + "s")
    return info_relationship

def testRelationship():
    #读取数据
    info_relationship = loadRelationship()
    #导出数据
    time_start = time.time()
    print("导出 relationship 数据中...")
    with open('A_relationship.txt', 'w', encoding='utf-8') as file_output:
        count_info = 0
        for info_current in info_relationship:
            count_info = count_info + 1
            if count_info > 1:
                file_output.write('\n')
            file_output.write(str(count_info) + '\n')
            file_output.write(info_current.toString())
    
    print('数据量 : ' + str(count_info))
    time_end = time.time()
    time_use =  time_end - time_start
    print("用时 : " + str(time_use) + "s")

def loadTweet(count_max=0):
    time_start = time.time()
    print("读取 Tweets 文件中...")
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    
    info_tweet = []
    with open("R_Tweets.json", encoding='utf-8') as file_tweet:
        list_tweet = file_tweet.readlines()
        id_line = 0
        for line_tweet in list_tweet:
            id_line = id_line + 1
            if count_max > 0 and id_line > count_max:
                break
            if not line_tweet.startswith('{'):
                print("错误: 行:%d 内容:%s " % (id_line, line_tweet))
            else:
                #创建一个对象
                info_current = Tweet()
                #去掉前后的大括号
                line_tweet = line_tweet.replace('{', '')
                line_tweet = line_tweet.replace('}\n', '')
                #先排除content对后续断句的干扰
                strT_Content = ', Content='
                strT_ID = ', ID='
                indexT_Content = line_tweet.find(strT_Content)
                indexT_ID = line_tweet.find(strT_ID)
                info_current.content = line_tweet[indexT_Content + len(strT_Content):indexT_ID]
                line_tweet = line_tweet[:indexT_Content] + line_tweet[indexT_ID:]
                
                #正常断句
                #用逗号分成子字符串
                try:
                    column_tweet = line_tweet.split(', ')
                    for columnT in column_tweet:
                        #print(columnT)
                        if columnT.startswith('_id='):
                            info_current._id = columnT[columnT.find('=')+1:]
                        elif columnT.startswith('Comment='):
                            info_current.comment = columnT[columnT.find('=')+1:]
                            info_current.comment = int(float(info_current.comment))
                        elif columnT.startswith('ID='):
                            info_current.id = columnT[columnT.find('=')+1:]
                            info_current.id = int(info_current.id)
                        elif columnT.startswith('Like='):
                            info_current.like = columnT[columnT.find('=')+1:]
                            info_current.like = int(float(info_current.like))
                        elif columnT.startswith('PubTime='):
                            info_current.pubTime = columnT[columnT.find('=')+1:]
                        elif columnT.startswith('Transfer='):
                            info_current.transfer = columnT[columnT.find('=')+1:]
                            info_current.transfer = int(float(info_current.transfer))
                        elif columnT.startswith('Co_oridinates='):
                            info_current.co_oridinates = columnT[columnT.find('=')+1:]
                        elif columnT.startswith('Tools='):
                            info_current.tools = columnT[columnT.find('=')+1:]
                        else:
                            print("未知: " + columnT)
                    str_date = info_current.pubTime
                    if str_date.find('-') > -1:
                        str_date = str_date[:str_date.find(' ')]
                        str_date = str_date.split('-')
                        info_current.year = int(str_date[0])
                        info_current.month = int(str_date[1])
                        info_current.day = int(str_date[2])
                    elif str_date.find('月') > -1:
                        info_current.year = 2017
                        info_current.month = int(str_date[:str_date.find('月')])
                        info_current.day = int(str_date[str_date.find('月')+1:str_date.find('日')])
                    elif str_date.find('今天') > -1:
                        info_current.year = 2017
                        info_current.month = 4
                        info_current.day = 20
                    elif str_date.find('分钟前') > -1:
                        info_current.year = 2017
                        info_current.month = 4
                        info_current.day = 20
                    
                    info_tweet.append(info_current)
                except Exception as e:
                    print (e)
                    print ("line = " + str(id_line))

    count = len(info_tweet)
    print("数据量 : %d" % count)
    time_end = time.time()
    time_use = time_end- time_start
    print("用时 : " + str(time_use) + "s")
    return info_tweet

def testTweet():
    #获取数据
    info_tweet = loadTweet()
    #导出数据
    time_start = time.time()
    print("导出 tweet 数据中...")
    with open('A_tweet.txt', 'w', encoding='utf-8') as file_output:
        count = 0
        for info_current in info_tweet:
            count = count + 1
            if count > 1:
                file_output.write('\n')
            file_output.write(str(count) + '\n')
            file_output.write(info_current.toString())
    
    print('数据量 : ' + str(count))
    time_end = time.time()
    time_use = time_end- time_start
    print("用时 : " + str(time_use) + "s")

def loadInformation(count_max=0):
    time_start = time.time()
    print("读取 Information 文件中...")
    #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    
    info_information = []
    with open("R_Information.json", encoding='utf-8') as file_information:
        list_information = file_information.readlines()
        id_line = 0
        for line_information in list_information:
            id_line = id_line + 1
            if count_max > 0 and id_line > count_max:
                break
            if not line_information.startswith('{'):
                print("错误: 行:%d 内容: %s" % (id_line, line_information))
            else:
                #创建一个对象
                info_current = Information()
                #去掉前后的大括号
                line_information = line_information.replace('{', '')
                line_information = line_information.replace('}\n', '')
                
                #排除BriefIntroduction的影响
                strT_BriefIntroduction = ', BriefIntroduction='
                indexT_BriefIntroduction = line_information.find(strT_BriefIntroduction)
                if indexT_BriefIntroduction > 0:
                    info_current.briefIntroduction = line_information[indexT_BriefIntroduction + len(strT_BriefIntroduction):]
                    line_information = line_information[:indexT_BriefIntroduction]

                #排除URL的影响
                #, URL=从业者, 从事互联网产品设计和策划、网站运营等工作。关注医院平台网络营销。】现担任北京巨龙副总。, Gender=男
                strT_URL = ', URL='
                indexT_URL = line_information.find(strT_URL)
                strT_Gender = ', Gender='
                indexT_Gender = line_information.find(strT_Gender)
                info_current.url = line_information[indexT_URL + len(strT_URL):indexT_Gender]
                line_information = line_information[:indexT_URL] + line_information[indexT_Gender:]

                #用逗号分成子字符串
                column_information = line_information.split(', ')
                for columnT in column_information:
                    #print(columnT)
                    if columnT.startswith('_id='):
                        info_current._id = columnT[columnT.find('=')+1:]
                        info_current._id = int(info_current._id)
                    elif columnT.startswith('Num_Follows='):
                        info_current.num_Follows = columnT[columnT.find('=')+1:]
                        info_current.num_Follows = int(float(info_current.num_Follows))
                    elif columnT.startswith('City='):
                        info_current.city = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Num_Tweets='):
                        info_current.num_Tweets = columnT[columnT.find('=')+1:]
                        info_current.num_Tweets = int(float(info_current.num_Tweets))
                    elif columnT.startswith('AvatarLink='):
                        info_current.avatarLink = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Province='):
                        info_current.province = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Gender='):
                        info_current.gender = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('Num_Fans='):
                        info_current.num_Fans = columnT[columnT.find('=')+1:]
                        info_current.num_Fans = int(float(info_current.num_Fans))
                    elif columnT.startswith('Birthday='):
                        info_current.birthday = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('InsertTime='):
                        info_current.insertTime = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('avatar_saved='):
                        info_current.avatar_saved = columnT[columnT.find('=')+1:]
                        info_current.avatar_saved = int(info_current.avatar_saved)
                    elif columnT.startswith('VIPlevel='):
                        info_current.viplevel = columnT[columnT.find('=')+1:]
                    elif columnT.startswith('NickName='):
                        info_current.nickName = columnT[columnT.find('=')+1:]
                    else:
                        print("未知: " + columnT)
                info_information.append(info_current)
    
    count = len(info_information)
    print("数据量 : %d" % count)
    time_end = time.time()
    time_use = time_end - time_start
    print("用时 : " + str(time_use) + "s")
    return info_information

def testInformation():
    #获取数据
    info_information = loadInformation()
    #导出数据
    time_start = time.time()
    print("导出数据中...")
    with open('A_information.txt', 'w', encoding='utf-8') as file_output:
        count_info = 0
        for info_current in info_information:
            count_info = count_info + 1
            if count_info > 1:
                file_output.write('\n')
            file_output.write(str(count_info) + '\n')
            file_output.write(info_current.toString())
    
    print('数据量 : ' + str(count_info))
    time_end = time.time()
    time_use = time_end - time_start
    print("用时 : " + str(time_use) + "s")



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
    def getID(cls):
        cls.id_now = cls.id_now + 1
        return cls.id_now

    def __init__(self):
        self.ID = Relationship.getID()
        self._id = 0
        self.host1 = 0
        self.host2 = 0

    def toString(self):
        strR = '\
ID = %d\n\
_id = %d\n\
host1 = %d\n\
host2 = %d\n'\
                % (\
                    self.ID, \
                    self._id, \
                    self.host1, \
                    self.host2)
        return strR

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
    def getID(cls):
        cls.id_now = cls.id_now + 1
        return cls.id_now

    def __init__(self):
        self.ID = Tweet.getID()
        self._id = ''
        self.comment = 0
        self.content = ''
        self.id = 0
        self.like = 0
        self.pubTime = ''
        self.transfer = 0
        self.co_oridinates = ''
        self.tools = ''
        self.year = 0
        self.month = 0
        self.day = 0

    def toString(self):
        strR = '\
ID = %d\n\
_id = %s\n\
Comment = %d\n\
Content = %s\n\
ID = %d\n\
Like = %d\n\
PubTime = %s\n\
Transfer = %d\n\
Co_oridinates = %s\n\
Tools = %s\n\
year-month-day = %d-%d-%d\n' \
                % (\
                    self.ID, \
                    self._id, \
                    self.comment, \
                    self.content, \
                    self.id, \
                    self.like, \
                    self.pubTime, \
                    self.transfer, \
                    self.co_oridinates, \
                    self.tools, \
                    self.year, \
                    self.month, \
                    self.day)
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
    def getID(cls):
        cls.id_now = cls.id_now + 1
        return cls.id_now

    def __init__(self):
        self.ID = Information.getID()
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

    def toString(self):
        strR = '\
ID = %d\n\
_id = %d\n\
Num_Follows = %d\n\
City = %s\n\
Num_Tweets = %d\n\
AvatarLink = %s\n\
Province = %s\n\
URL = %s\n\
Gender = %s\n\
Num_Fans = %d\n\
Birthday = %s\n\
InsertTime = %s\n\
avatar_saved = %d\n\
VIPLevel = %s\n\
NickName = %s\n\
BriefIntroduction = %s\n'  \
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

if __name__ == "__main__":
    testInformation()
    testRelationship()
    testTweet()

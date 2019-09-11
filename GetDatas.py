import re
import os
import Data

soundfile = []

class author:   #作者类
    def __init__(self):
        self.name = ""
        self.id = 0
        self.fans = 0   #粉丝数
        self.list_tweets = [] #微博列表  


# class Tweet:    #微博类
#     id_now = -1
#     @classmethod
#     def GetID(cls):
#         cls.id_now = cls.id_now + 1
#         return cls.id_now

#     def __init__(self):
#         self.ID = Tweet.GetID()
#         self.content = ''
#         self.content_old = ''
#         self.comment = 0
#         self.like = 0
#         self.transfer = 0
#         self.year = 0
#         self.month = 0
#         self.day = 0
#         self.value = 0
#         self.dict_words_tfidf = {}
#         self.error = ''
#         self.id_author = 0 #作者id
#         self.id_hotspot = 0 #热点id
#         self.pubTime = ''

#     def ToString(self):
#         strR = '\
# ID = [ %d ]\n\
# Content = [ %s ]\n\
# Content(old) = [ %s ]\n\
# Comment = [ %d ]\n\
# Like = [ %d ]\n\
# Transfer = [ %d ]\n\
# year = [ %d ]\n\
# month = [ %d ]\n\
# day = [ %d ]\n\
# value = [ %d ]\n\
# dict_words_tfidf = [ %s ]\n\
# error = [ %s ]\n\
# ID(author) = [ %d ]\n\
# ID(hotspot) = [ %d ]\n\
# ' % (\
#         self.ID, \
#         self.content, \
#         self.content_old, \
#         self.comment, \
#         self.like, \
#         self.transfer, \
#         self.year, \
#         self.month, \
#         self.day, \
#         self.value, \
#         str(self.dict_words_tfidf), \
#         self.error, \
#         self.id_author, \
#         self.id_hotspot)

#         return strR
        ''' 

class Tweet:       #微博类
    _id_now = 0
    @classmethod
    def getID(cls):
        cls._id_now += 1
        return cls._id_now
    def __init__(self):
        self.ID = Tweet.getID()   #自动取得ID
        self.content = ""   #博文
        self.like = 0  #点赞数
        self.transfer = 0   #转发数
        self.comment = 0    #评论数
        self.time = 0
        
'''

def GetMiddleStr(content,startStr,endStr):
    patternStr = r'%s(.+?)%s'%(startStr,endStr)
    p = re.compile(patternStr,re.IGNORECASE)
    m= re.match(p,content)
    if m:
        return m.group(1)

def eachfile(filepath):
    pathdir = os.listdir(filepath)
    for s in pathdir:
        newdir = os.path.join(filepath, s)  # 将文件名加入到当前文件路径后面
        if os.path.isfile(newdir):  # 如果是文件
            if os.path.splitext(newdir)[1] == ".txt":  # 如果文件是".pdb"后缀的
                soundfile.append(newdir)
        elif os.path.isdir(newdir):  # 如果是路径
            eachfile(newdir)  # 递归
    return soundfile

def GetListAuthors(fp):
    list_authors = []
    index = 8   #开始储存微博内容处
    f =  eachfile(fp)   #获取txt文件列表
    lencont = 0 #统计推文数量

    for fi in f:
    #fi = f[0]
        with open(fi, "r", encoding="utf-8") as file_tweets:
            authorT = author()
            authorT.name = ""
            authorT.like = 0
            authorT.list_tweets = []
            list_datas = file_tweets.readlines()    #将文件以列表读取
            index = 8
            lendatas = len(list_datas)  #获取的文件长度
            '''
            print("index = %d" % index)
            print("lendates = %d" % lendatas)
            '''

            for i in range(6):
                if i == 0:
                    continue    
                elif i == 1:
                    authorT.name = GetMiddleStr(list_datas[i],'用户昵称：','\n')
                    #print(authorT.name)
                elif i == 2:
                    authorT.id = int(GetMiddleStr(list_datas[i],'用户id: ','\n'))
                    #print(authorT.id)
                elif i == 3:
                    continue 
                elif i == 4:
                    continue 
                elif i == 5:
                    authorT.fans = int(GetMiddleStr(list_datas[i],'粉丝数: ','\n'))
                    #print(authorT.fans)
            
            while index < lendatas:
                '''
                if (index-8)%6 != 0:
                    print("error_index = %d" % index)
                    break
                '''

                line = list_datas[index]
                if len(line) < 1:
                    print("konghang")
                    break
                                                    
                tweetT = Data.Tweet()
                #微博文本
                weibo_content = list_datas[index]
                eliminate_1 = re.compile(r" [^ ]+的微博视频")
                weibo_content = eliminate_1.sub('',weibo_content)
                eliminate_2 = re.compile(r"@[\u4e00-\u9fa5a-zA-Z0-9_-]{4,30}")
                weibo_content = eliminate_2.sub('',weibo_content)
                eliminate_3 = re.compile(r"[组图共[0-9]张")
                weibo_content = eliminate_3.sub('',weibo_content)
                weibo_content = weibo_content.replace(" ","")   #去空格
                tweetT.content = weibo_content[weibo_content.find(':')+1 : -1]
                #发布时间
                weibo_time = list_datas[index+2]
                str_date = weibo_time[weibo_time.find('发布时间: ')+6 : -1]
                if str_date.find('-') > -1:
                    str_date = str_date[:str_date.find(' ')]
                    str_date = str_date.split('-')
                    tweetT.year = int(str_date[0])
                    tweetT.month = int(str_date[1])
                    tweetT.day = int(str_date[2])
                #作者id
                tweetT.id_author = authorT.id
                #点赞数
                weibo_data = list_datas[index+3]
                tweetT.like = int(GetMiddleStr(weibo_data,'点赞数: ','   转发数: '))
                #评论数
                tweetT.transfer = int(weibo_data[weibo_data.find('转发数: ')+5 : weibo_data.find('   评论数: ')])
                #转发数
                tweetT.comment = int(weibo_data[weibo_data.find('评论数: ')+5 : -1])
                '''
                print('\n')
                print(index,end="   ")
                print(lendatas)
                print(tweetT.content)
                print(tweetT.time)
                print(tweetT.likes)
                print(tweetT.tran)
                print(tweetT.comment)
                print('\n')
                '''

                index += 6
                #print(line)
                authorT.list_tweets.append(tweetT)

            #lencont += len(authorT.list_tweets)
        
            list_authors.append(authorT)
            #print(authorT.name)

    #print(lencont)
        

    return list_authors

def out_tweetlist(authors_list,filename):
    tweet_data = open(filename, "w+", encoding='utf-8')
    for authort in authors_list:
        for Tweet_now in authort.list_tweets:
            tweet_data.write(Tweet_now.ToString())
            tweet_data.write("\n")
    tweet_data.close()

def out_authorlist(authors_list,filename):
    author_name = open(filename, "w+", encoding='utf-8')
    for authort in authors_list:
        author_name.write(authort.name)
        author_name.write("\n")
    author_name.close()


def main():
    authors_list = []
    authors_list = GetListAuthors("weiboSpider-master\weibo")
    out_authorlist(authors_list,"output/authors_name")
    out_tweetlist(authors_list,"output/datas_tweets.txt")


if __name__ == "__main__":
    main()

    
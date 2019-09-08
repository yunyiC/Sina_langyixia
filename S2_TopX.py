
import time
import S1_Data

def compareByComment(itemA, itemB):
    return (itemA.comment > itemB.comment)

def compareByLike(itemA, itemB):
    return (itemA.like > itemB.like)

def compareByTransfer(itemA, itemB):
    return (itemA.transfer > itemB.transfer)

class TopX:
    def __init__(self, func_compare):
        self.topX = []
        self.id_last = -1 #指向最后一个元素
        self.compare = func_compare

    def push(self, item):
        isChanged = False
        if self.id_last < 9:
            self.topX.append(item)
            self.id_last = self.id_last + 1
            isChanged = True
        else:
            if self.compare(item, self.topX[self.id_last]) :
                self.topX[self.id_last] = item
                isChanged = True
        if isChanged:
            id_now = self.id_last
            itemT = self.topX[id_now]
            while id_now > 0:
                if self.compare(itemT, self.topX[id_now-1]):
                    self.topX[id_now] = self.topX[id_now-1]
                    id_now = id_now - 1
                else:
                    break
            self.topX[id_now] = itemT
    
    def output(self, filename):
        with open(filename, "w", encoding='utf-8') as file_output:
            count = 0
            for itemT in self.topX:
                count = count + 1
                file_output.write("%d\n" % count)
                file_output.write(itemT.toString())
                file_output.write("\n")
            print("共有 %d 条数据" % count)

if __name__ == "__main__":
    # info_information = MData.MData.loadInformation()
    # info_relationship = MData.MData.loadRelationship()
    info_tweet = S1_Data.loadTweet()

    time_start = time.time()
    print('处理数据中...')
    topX_comment = TopX(compareByComment)
    topX_like = TopX(compareByLike)
    topX_transfer = TopX(compareByTransfer)
    for info in info_tweet:
        topX_comment.push(info)
        topX_like.push(info)
        topX_transfer.push(info)
    time_end = time.time()
    time_use = time_end - time_start
    print("用时 : " + str(time_use) + "s")

    #导出数据
    time_start = time.time()
    print("导出数据中...")

    topX_comment.output("B_TopX_comment.txt")
    topX_like.output("B_TopX_like.txt")
    topX_transfer.output("B_TopX_transfer.txt")

    time_end = time.time()
    time_use = time_end - time_start
    print("用时 : " + str(time_use) + "s")

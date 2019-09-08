
import S1_Data

class MDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def MoreThan(self, dateOther):
        if self.year > dateOther.year:
            return True
        elif self.year == dateOther.year:
            if self.month > dateOther.month:
                return True
            elif self.month == dateOther.month:
                if self.day > dateOther.day:
                    return True
                elif self.day == dateOther.day:
                    return True
        return False

    def LessThan(self, dateOther):
        if self.year < dateOther.year:
            return True
        elif self.year == dateOther.year:
            if self.month < dateOther.month:
                return True
            elif self.month == dateOther.month:
                if self.day < dateOther.day:
                    return True
                elif self.day == dateOther.day:
                    return True
        return False
            
def SaveTweetsByDate(date_start, date_end):
    infos_tweet = S1_Data.loadTweet()
    list_tweets = []

    for info in infos_tweet:
        date = MDate(info.year, info.month, info.day)
        if date.MoreThan(date_start) and date.LessThan(date_end):
            list_tweets.append(info)
    
    with open("E_tweets_by_date", "w", encoding="utf-8") as file_result:
        for tweet in list_tweets:
            file_result.write(tweet.toString())
            file_result.write("\n")

if __name__ == "__main__":
    date_start = MDate(2016, 1, 1)
    date_end = MDate(2016, 12, 31)
    SaveTweetsByDate(date_start, date_end)

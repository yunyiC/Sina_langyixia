
import S1_Data

class data():
    def __init__(self):
        self.max_year = 0
        self.max_month = 0
        self.max_day = 0

        self.min_year = 2020
        self.min_month = 0
        self.min_day = 0

    def save_max(self, year, month, day):
        self.max_year = year
        self.max_month = month
        self.max_day = day
    
    def save_min(self, year, month, day):
        self.min_year = year
        self.min_month = month
        self.min_day = day


if __name__ == "__main__":
    info_tweet = S1_Data.loadTweet()

    dataT = data()

    for info in info_tweet:
        year = info.year
        month = info.month
        day = info.day

        if year > dataT.max_year:
            dataT.save_max(year, month, day)
        elif year == dataT.max_year:
            if month > dataT.max_month:
                dataT.save_max(year, month, day)
            elif month == dataT.max_month:
                if day > dataT.max_day:
                    dataT.save_max(year, month, day)

        if year < dataT.min_year:
            dataT.save_min(year, month, day)
        elif year == dataT.min_year:
            if month < dataT.min_month:
                dataT.save_min(year, month, day)
            elif month == dataT.min_month:
                if day < dataT.min_day:
                    dataT.save_min(year, month, day)

    with open("A_date_result.txt", 'w', encoding='utf-8') as file_result:
        file_result.write("最大日期 : %d-%d-%d\n" % (dataT.max_year, dataT.max_month, dataT.max_day))
        file_result.write("最小日期 : %d-%d-%d\n" % (dataT.min_year, dataT.min_month, dataT.min_day))
    
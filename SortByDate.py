
import Data
import os

if __name__ == "__main__" :
    infos_tweet = Data.GetListTweets("output/pretreatment_result.txt")
    dict_files = {}
    for info in infos_tweet:
        year = '{:0>2}'.format(str(info.year))
        month = '{:0>2}'.format(str(info.month))
        day = '{:0>2}'.format(str(info.day))
        
        filename = os.path.dirname(os.path.realpath(__file__)) + "\\date\\" + year + "-" + month + "-" + day + ".txt"
        if filename not in dict_files :
            dict_files[filename] = open(filename, "w+", encoding="utf-8")
        dict_files[filename].write(info.ToString())
        dict_files[filename].write("\n")
    
    for fileT in dict_files.values() :
        fileT.close()

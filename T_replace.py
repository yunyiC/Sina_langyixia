
filenames=['Information.json','Relationships.json','Tweets.json']
# filename = filenames[2]
filename = "output_dict_cluster.txt"
str1=r"],"
str2=r"],\n"

import re
print("替换中...")
f=open(filename,'r',encoding='utf-8')
alllines=f.readlines()
f.close()
print("保存中...")
f=open(filename,'w+',encoding='utf-8')
for eachline in alllines:
    a=re.sub(str1,str2,eachline)
    f.writelines(a)
f.close()
print ("完成")
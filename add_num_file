import csv
import glob
import os
from natsort import natsorted

path = '/Users/yasuhiko/PycharmProjects/bow 3.7 jp not lsi/result/*.txt'
i = 1
lists = []
flist = glob.glob(path)
num=1
num2=1
count=1
for file in natsorted(flist):
    with open(file, 'r') as f:
        lines2 = f.readlines()  # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        f.close()
        line = []
        if num2==30:
            num2=1
        if (count%30)==0:
            num+=1

        for oneline in lines2:
            line=str(num)+'-'+str(num2)+','+ oneline
            f = open('/Users/yasuhiko/PycharmProjects/bow 3.7 jp not lsi/result2/test2', 'a')
            f.write(line + '\n')
            f.close()
    num2+=1
    count+=1

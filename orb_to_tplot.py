#remot path = 'http://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/'
path = './orbit/19890301.orb'

with open(path) as f:
    datalist = f.readlines()
    for i in range(len(datalist)):
        datalist[i] = datalist[i].split() 

for i in range(5):
    print(datalist[i])

url = 'https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/201401/ED140101.txt'
import os 
import urllib.request
get_data = urllib.request.urlopen(url).readlines()
try:
    with open(save_name, mode="wb") as f:
        f.write(get_data)
except:
    pass
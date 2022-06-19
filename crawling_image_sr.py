import requests
import re
import os
import time
from bs4 import BeautifulSoup
from io import BytesIO

r = open('sr_sample.txt', mode='rt', encoding='utf-8')
url_list_origin = []
file_name_list = []
idx = 0
for line in r:
    idx = idx + 1
    temp = line.split('^')
    temp_url = re.sub('\n','',temp[0])
    url = re.sub('r_','_',temp_url)
    if temp[0] != '기사 ID':
        if url not in url_list_origin:
            url_list_origin.append(url)
            temp1 = temp[1].split(' ')
            idx_len = 0
            if len(str(idx)) < 2 :
                idx_len = -2
            else :
                idx_len = -1*len(str(idx))
            file_name_list.append(re.sub('[\\/:*?"<>|]','',('조선왕조실록_'+temp1[0]+'_苧布_'+('0'+str(idx))[idx_len:]).strip()))
r.close()

index = 0
for url in url_list_origin:
    print(str(index)+':'+url)
    origin_url = 'http://sillok.history.go.kr/popup/viewer.do?type=view&id='+url
    res = requests.get(origin_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    script = soup.select('script')
    start = script[9].string.find('imgArr = [')
    end = script[9].string.find('hlArr = [')
    temp_res = re.sub('\n', '',script[9].string[start:end]).strip()
    end2 = temp_res.find('];')
    temp_img_list = re.sub('"','',temp_res[10:end2])
    img_list = temp_img_list.replace('\\','').split(',')
    
    time.sleep(0.5)
    
    for i in range(len(img_list)) :
        file_name = file_name_list[index]
        if len(img_list) > 1:
            file_name = file_name +'_'+('0'+str(i+1))[-2:]+'.jpg'
        else :
            file_name = file_name + '.jpg'

        res2 = requests.get('http://sillok.history.go.kr/viewer/imageProxy.do?filePath=/s_img/SILLOK/' + img_list[i] + '.jpg')
        
        path = './images/'

        try:
            if not(os.path.isdir(path)):
                os.makedirs(os.path.join(path))
        except OSError:
            print("Failed to create directory!!!!!")

        with open(path+file_name, 'wb') as f:
            f.write(BytesIO(res2.content).read())
        
        time.sleep(1)
            
    index = index + 1
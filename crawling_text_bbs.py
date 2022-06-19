import requests
import re
import os
from bs4 import BeautifulSoup

r = open('bbs_sample22.txt', mode='rt', encoding='utf-8')
url_list_origin = []
url_list_trans = []

for line in r:
    temp = line.split('^')
    temp_url = re.sub('\n','',temp[0])
    url = re.sub('r_','_',temp_url)
    if temp[0] != '자료ID':
        if url not in url_list_origin:
            url_list_origin.append(url)
            url_list_trans.append(url[0:6]+'r'+url[6:])
        
r.close()

all_contents = "아이디"+"\t"+"연번"+"\t"+"품목"+"\t"+"시기"+"\t"+"기사제목"+"\t"+"원문"+"\t"+"번역문"+"\t"+"분류"+"\t"+"소분류"+"\t"+"출처"+"\t"+"출처-링크"+"\t"+"관련 내용"+"\t"+"원문이미지 수집 여부"+"\t"+"관련국가"+"\t"+"유통경로\r\n"
index = 0
for url in url_list_origin:
    print(str(index)+':'+url)
    origin_url = 'http://db.history.go.kr/id/'+url
    trans_url = 'http://db.history.go.kr/id/'+url_list_trans[index]
    res = requests.get(origin_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    res2 = requests.get(trans_url)
    soup2 = BeautifulSoup(res2.content, 'html.parser')
    index = index + 1
    
    seq = str(index) #연번
    item = '人蔘' #품목
    time = '' #시기
    title = '' #기사제목
    origin = '' #원문
    trans = '' #번역문
    source = '' #출처
    source_link = '' #출처-링크
    check_time = soup.select('.dl_data_pru')[0].findAll('td')
    if len(check_time) > 1:
        temp_time = re.sub('\xa0',' ',check_time[1].get_text())
        list_time = temp_time.split(' ')
        time = list_time[2]+'('+list_time[0]+re.sub('년','',list_time[1])+')'
    
        title = re.sub('\n','',check_time[0].get_text()).strip()
        origin_temp = re.sub('\n','',soup.select('#cont_view')[0].get_text().strip()) 
        origin = re.sub('\t',' ',origin_temp) 
        trans_temp = re.sub('\n','',soup2.select('#cont_view')[0].get_text().strip()) 
        trans = re.sub('\t',' ',trans_temp) 
    
        source_temp = soup.select('.cont_location')[0].findAll('a') 
        source = (re.sub('>','',source_temp[0].get_text()).strip() + ' ' + temp_time).strip()
    
    source_link = origin_url
    all_contents += " "+"\t"+seq+"\t"+item+"\t"+time+"\t"+title+"\t"+origin+"\t"+trans+"\t"+" "+"\t"+" "+"\t"+source+"\t"+source_link+"\t"+" "+"\t"+" "+"\t"+" "+"\t"+" "+"\r\n"

file = open('result.txt','wb')
file.write(all_contents.encode('utf-8'))
file.close()
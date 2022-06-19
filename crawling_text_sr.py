import requests
import re
import os
from bs4 import BeautifulSoup

r = open('sample3.txt', mode='rt', encoding='utf-8')
url_list = []

for line in r:
    temp = line.split('^')
    url = re.sub('\n','',temp[len(temp)-1])
    url_list.append(url)

r.close()

all_contents = "위치"+"\t"+"날짜"+"\t"+"제목"+"\t"+"번역"+"\t"+"원문\r\n"
for url in url_list:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    tit_loc = soup.select('.tit_loc')[0]

    date_text = ''
    for span in tit_loc.findAll('span'):
        date_text = re.sub('[\n\r\t]','',span.get_text().strip())
        span.extract()
    loc_text = re.sub('[\n\r\t]','',tit_loc.get_text().strip())

    title = soup.select('h3.search_tit')[0]
    title_text = re.sub('[\n\r\t]','',title.get_text().strip())

    contents = soup.select('div.ins_view_pd')
    content_text = []
    for content in contents:
        temp = ''
        for paragraph in content.findAll('p','paragraph'):
            for ul in paragraph.findAll('ul'):
                ul.extract()
            temp += paragraph.get_text()
        content_text.append(re.sub('[\n\r\t]','',temp.strip()))
        temp = ''
    
    all_contents += loc_text+'\t'+date_text+'\t'+title_text+'\t'+content_text[0]+'\t'+content_text[1]+'\r\n'

file = open('result.txt','wb')
file.write(all_contents.encode('utf-8'))
file.close()
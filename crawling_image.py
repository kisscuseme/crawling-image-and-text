from selenium import webdriver
import base64
import re
import os
import time

r = open('sample2.txt', mode='rt', encoding='utf-8')
id_list = []
idx = 0

for line in r:
    idx = idx + 1
    temp = line.split('^')
    id = temp[0]
    #file_name = re.sub('[\\/:*?"<>|]','',(temp[1]+'_'+temp[2]+'_'+temp[3]).strip())+'.png' #조선왕조실록_태종실록_苧布_01_02
    temp1 = temp[1].split(' ')
    idx_len = 0
    if len(str(idx)) < 2 :
        idx_len = -2
    else :
        idx_len = -1*len(str(idx))
    file_name = re.sub('[\\/:*?"<>|]','',('조선왕조실록_'+temp1[0]+'_苧布_'+('0'+str(idx))[idx_len:]).strip())
    id_list.append([id, file_name])

r.close()

browser = webdriver.Chrome('./chromedriver')

for i, v in enumerate(id_list):
    print(i)
    browser.get('http://sillok.history.go.kr/popup/viewer.do?type=view&id='+v[0]) #http://sillok.history.go.kr/viewer/imageProxy.do?filePath=/s_img/SILLOK/da/ida_d008005a00.jpg
    total_page = browser.execute_script("return document.querySelectorAll('#total_page')[0].innerText")
    for i in range(int(total_page)) :
        file_name = v[1]
        if int(total_page) > 1:
            file_name = file_name +'_'+('0'+str(i+1))[-2:]+'.png'
        else :
            file_name = file_name + '.png'
            
        if i > 0 :
            browser.find_element_by_xpath('//*[@id="next"]').click()
            time.sleep(1)
        base64_image = browser.execute_script("return document.querySelector('canvas').toDataURL('image/png').substring(21);")
        output_image = base64.b64decode(base64_image)
        path = './images/'

        try:
            if not(os.path.isdir(path)):
                os.makedirs(os.path.join(path))
        except OSError:
            print("Failed to create directory!!!!!")

        with open(path+file_name, 'wb') as f:
            f.write(output_image)
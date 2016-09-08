
# -*- coding: utf-8 -*-
import os
import time
import random
import requests
import logging
from RandomHeader import getHeaders
from RecognizeVCode import crackVcode

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

url = "http://wenshu.court.gov.cn/List/ListContent"

def getpageinfo():
    n = 1
    max_num = 1000
    url_source = 'wget  -P ./page http://wenshu.court.gov.cn/List/ListContent --post-data="Param=%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&Index={}&Page={}&Order=%E6%B3%95%E9%99%A2%E5%B1%82%E7%BA%A7&Direction=asc"'
    while(n<max_num):
        url = url_source.format(n,5)
        os.system(url)
        n = n + 1
        print n
        time.sleep(10)  # 休眠1秒

def getPageInfo(url, page_idx):

    data = {
        'Param':'文书类型:判决书',
        'index': page_idx,
        'Page':20,
        'Order':'法院层级',
        'Direction':'asc'
    }

    """
    # try proxy
    proxies = {'http': '127.0.0.1:3128'}
    proxies = {'http': '201.55.85.174:3128'}

    print requests.post(url=url, data=data, proxies = proxies).content
    """
    
    headers = getHeaders()
    response = requests.post(url=url, data=data, headers=headers)
    return response

def downloadPages(file, start_page, stop_page):

    def verify(content):
        return len(content) > 40

    def _checkpoint(idx):
        if ((idx-start_page)%20 == 1) or (idx >= stop_page):
            with open(file,'wb') as f:
                f.write(contents)

    
    tryout = 0
    idx = start_page
    contents = 'start\n'
    while(idx <= stop_page):
        _checkpoint(idx)

        logging.info("try obtain page: %d"%idx)
        response = getPageInfo(url, idx)
        content = response.content
        success = verify(content)
        if success:
            contents = contents+"page No.:%d \n"%idx+content+"\n\n"

            logging.info("success")
            tryout = 0
            idx += 1
        else:
            tryout += 1
            logging.info("failed, tried %d times"%tryout)
            _,res = crackVcode()
            logging.info("crack reault: %s (1: success, 2: failed)"%res)
            if int(res) == 1:
                #time.sleep(20) #after test this "waiting trick" does not work

        if tryout > 20:
            logging.info("exceed maximum tryouts")
            break

        time.sleep(0.5+0.5*random.random())

    _checkpoint(idx)
    logging.info("finished download %d ~ %d pages"%(start_page, idx-1)) 




if __name__ == '__main__':
    logging.info('start')
    file_path = os.path.join(os.path.split(__file__)[0],'pageinfo.txt')
    downloadPages(file_path, 1, 400)

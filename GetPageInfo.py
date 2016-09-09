
# -*- coding: utf-8 -*-
import os,sys
import time
import random
import requests
import logging
import datetime
from RandomHeader import getHeaders
from RecognizeVCode import crackVcode
import pdb

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


def getPageInfo(url, page_idx, search_params):

    data = {
        'Param': search_params,
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
    rndcookie = random.randint(100, 999)

    headers = {
    'Host': 'wenshu.court.gov.cn',
    'Connection': 'keep-alive',
    'Content-Length': 153,
    'Accept': '*/*',
    'Origin': 'http://wenshu.court.gov.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+%E5%88%A4%E5%86%B3%E4%B9%A6+++%E6%96%87%E4%B9%A6%E7%B1%BB%E5%9E%8B:%E5%88%A4%E5%86%B3%E4%B9%A6',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }

    cookies = {
        'ASP.NET_SessionId':'3ks3gtwmyrfnqdsjmvetvqp5', 
        'wafenterurl=/List/List': 'wafcookie=a12defabf56a5562db7cb80c216203a4',
        '__utma': '61363882.568771455.1473331186.1473331186.1473331186.1',
        '__utmc': '61363882',
        '__utmz': '61363882.1473331186.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'JSESSIONID': 'aaaD5WhpFlEi6e4nUP8Bv',
        'Hm_lvt_3f1a54c5a86d62407544d433f6418ef5': '1472542915,1472543876,1473311822,1473311827',
        'Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5': '1473390%d'%rndcookie, 
        '_gsref_2116842793': 'http://wenshu.court.gov.cn/', 
        '_gscu_2116842793': '71588436x2efq281', 
        '_gscs_2116842793': 't73389711qxmxto12|pv:7; _gscbrs_2116842793=1'
    }
    response = requests.post(url=url, data=data, headers=headers, cookies = cookies)
    return response

def downloadPages(file, start_page, stop_page, search_params):

    def verify(content):
        return len(content) > 40

    def _checkpoint(idx, contents):
        if ((idx-start_page)%20 == 19) or (idx >= stop_page):
            with open(file,'a') as f:
                f.write(contents)
            return ''

        else:
            return contents

    def _write2file():
        if len(contents) > 6:
            with open(file,'a') as f:
                    f.write(contents)

    
    tryout = 0
    idx = start_page
    contents = ''
    while(idx <= stop_page):
        contents = _checkpoint(idx, contents)

        logging.info(search_params+"try obtain page: %d"%idx)
        response = getPageInfo(url, idx, search_params)
        content = response.content
        success = verify(content)
        if success:
            contents = contents+search_params+"page No.:%d \n"%idx+content+"\n\n"

            logging.info("success")
            tryout = 0
            idx += 1
        else:
            tryout += 1
            logging.info("failed, tried %d times"%tryout)
            _,res = crackVcode()
            logging.info("crack result: %s (1: success, 2: failed)"%res)
            """if int(res) == 1:
                requests.get(url='http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+%E5%88%A4%E5%86%B3%E4%B9%A6+++%E6%96%87%E4%B9%A6%E7%B1%BB%E5%9E%8B:%E5%88%A4%E5%86%B3%E4%B9%A6',
                headers ={
                'Host': 'wenshu.court.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
                'Referer': 'http://wenshu.court.gov.cn/list/list/?sorttype=1',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                'Cookie': 'ASP.NET_SessionId=3ks3gtwmyrfnqdsjmvetvqp5; wafenterurl=/List/List; wafcookie=a12defabf56a5562db7cb80c216203a4; __utma=61363882.568771455.1473331186.1473331186.1473331186.1; __utmc=61363882; __utmz=61363882.1473331186.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=aaaD5WhpFlEi6e4nUP8Bv; _gsref_2116842793=http://wenshu.court.gov.cn/; _gscu_2116842793=71588436x2efq281; _gscs_2116842793=t73389711qxmxto12|pv:8; _gscbrs_2116842793=1; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1472542915,1472543876,1473311822,1473311827; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1473392%d'%(random.randint(100,999))
                })
                #time.sleep(20) #after test this "waiting trick" does not work
                pass"""

        if tryout > 1:
            logging.info("exceed maximum tryouts")
            break

        #time.sleep(0.1+0.1*random.random())

    _write2file()
    logging.info("finished download %d ~ %d pages"%(start_page, idx-1))

    if  idx > start_page:
        return True
    else:
        return False

def downloadPlan(start_page, stop_page):
    
    interval = 100 # 100 pages in a file

    idx = start_page
    while(idx<=stop_page): 
        pages = (idx, min(idx+interval-1, stop_page))

        logging.info("plan downloading page NO.%d - No.%d"%(pages[0],pages[1]))
        file_path = os.path.join(os.path.split(__file__)[0],
            'pageinfo%d-%d.txt'%(pages[0],pages[1]))

        success = downloadPages(file_path, pages[0], pages[1])

        if success:
            idx += interval


def processControl():

    states_list = ["北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省","吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省",
        "福建省","江西省","山东省","河南省","湖北省"]#,"湖南省","广东省","广西壮族自治区","海南省","重庆市","四川省","贵州省",
        #"云南省","西藏自治区","陕西省","甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","新疆维吾尔自治区高级人民法院生产建设兵团分院"]
    for state in states_list:

        file_path = os.path.join(os.path.split(__file__)[0],
            'pageinfo%s.txt'%state)

        for year in xrange(1996,2011):

            search_params = "文书类型:判决书,法院地域:{},裁判年份:{}".format(state,year)
            downloadPages(file_path, 1, 100, search_params)

        for year in xrange(2011,2013):
            for month in xrange(1,13):
                if month <12:
                    search_params = "文书类型:判决书,法院地域:{},裁判日期:{} TO {}".format(state, "%04d-%02d-01"%(year,month), "%04d-%02d-01"%(year,month+1))
                else:
                    search_params = "文书类型:判决书,法院地域:{},裁判日期:{} TO {}".format(state, "%04d-%02d-01"%(year,month), "%04d-%02d-01"%(year+1,1))
                downloadPages(file_path, 1, 100, search_params)



        for date in datelist((2013, 1, 1), (2016, 9, 9)):
            search_params = "文书类型:判决书,法院地域:{},裁判日期:{} TO {}".format(state, date, date)
            downloadPages(file_path, 1, 100, search_params)

            


def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result





if __name__ == '__main__':

    logging.info('start')

    """#downloadPlan(1, 400)
    start_page = int(sys.argv[1])
    stop_page = int(sys.argv[2])
    pages = (start_page, stop_page)

    logging.info("plan downloading page NO.%d - No.%d"%(pages[0],pages[1]))
    file_path = os.path.join(os.path.split(__file__)[0],
        'pageinfo%d-%d.txt'%(pages[0],pages[1]))

    success = downloadPages(file_path, pages[0], pages[1])"""

    processControl()


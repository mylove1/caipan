# -*- coding: utf-8 -*-
import os
import datetime
import time
import random
import requests
import logging
from RandomHeader import getHeaders
from RecognizeVCode import crackVcode
import sys

import threading

# area = ["北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省","吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省",
#         "福建省","江西省","山东省","河南省","湖北省","湖南省","广东省","广西壮族自治区","海南省","重庆市","四川省","贵州省",
#         "云南省","西藏自治区","陕西省","甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","新疆维吾尔自治区高级人民法院生产建设兵团分院"]
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
    while (n < max_num):
        url = url_source.format(n, 5)
        os.system(url)
        n = n + 1
        print n
        time.sleep(10)  # 休眠1秒


def getPageInfo(url, page_idx, start_date, end_date, areaName):  # 3,2012-09-11,2012-09-11,黑龙江省
    data = {
        'Param': '文书类型:判决书,裁判日期:{} TO {},法院地域:{}'.format(start_date, end_date, areaName),
        'index': page_idx,
        'Page': 20,
        'Order': '法院层级',
        'Direction': 'asc'
    }

    """
    # try proxy
    proxies = {'http': '127.0.0.1:3128'}
    proxies = {'http': '201.55.85.174:3128'}

    print requests.post(url=url, data=data, proxies = proxies).content
    """

    headers = getHeaders()
    # coo['Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5'] = '147339107'.format(page_idx%10)
    # cookiess = {'Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5': '147339107'.format(page_idx % 10)}
    response = requests.post(url=url, data=data, headers=headers)
    return response


def downloadPages(state):
    re_file_path = ('./page1/record{}.txt'.format(state))
    file_path = ('./page/info{}.txt'.format(state))

    # read
    re_file = open(re_file_path, 'r')
    source_ss = re_file.read()
    re_file.close()
    maps = source_ss.split('-')
    page_id = int(maps[0])
    date_year = int(maps[1])
    date_month = int(maps[2])
    date_day = int(maps[3])
    
    date1_year = int(maps[4])
    date1_month = int(maps[5])
    date1_day = int(maps[6])
    

    start_date = datetime.date(date_year, date_month, date_day)
    start_date1 = datetime.date(date1_year, date1_month, date1_day)

    def verify(content):
        return len(content) > 40

    def _checkpoint(content):
        # if ((idx-start_page)%20 == 1) or (idx >= stop_page):
        # file = "{}info.txt".format(state)
        with open(file_path, 'a') as f:
            f.write(content)

    # "北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "上海市", "江苏省", "浙江省", "安徽省",
    # "福建省", "江西省", "山东省", "河南省", "湖北省",
    # "重庆市","广东省", "广西壮族自治区", "海南省", "四川省", "贵州省",
    #                "云南省", "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", "新疆维吾尔自治区高级人民法院生产建设兵团分院"

    num_lxg = 0
    idx = page_id
    t = 1	
    
    for date in datelist(start_date1, (2016, 9, 9)):  # (2013,1,1),(2016,9,9)
        idx = page_id
        date_lxg = start_date
        date_lxg1 = date
        tryout = 0
        while (idx <= page_id+99):

            logging.info('try obtain page: {},文书类型:判决书,裁判日期:{} TO {},法院地域:{}'.format(idx, start_date, date, state))
            response = getPageInfo(url, idx, start_date, date, state)

            content = response.content
            success = verify(content)
            if success:
                contents = "文书类型:判决书,裁判日期:{} TO {},法院地域:{},page No.:{} \n\n".format(start_date, date, state, idx) + content
                _checkpoint(contents)
                logging.info("successful")
                tryout = 0
                idx += 1
                num_lxg += 1
            else:
                tryout += 1
                logging.info("failed, tried %d times" % tryout)
                _, res = crackVcode(state)
                logging.info("crack reault: %s (1: success, 2: failed)" % res)
                if int(res) == 1:
                     break
            time.sleep(2* random.random())  # after test this "waiting trick" does not work
            #
            if tryout > 10:
                logging.info("exceed maximum tryouts")
                break
            if (num_lxg >= 99):
                break
        page_id = 1
        start_date  = date
        if(num_lxg>=99):
            break
	logging.info('total---{}'.format(num_lxg))
    re_file = open(re_file_path, 'w')
    re_file.write("{}-{}-{}".format(idx, date_lxg, start_date))
    re_file.close()
    logging.info("finished download")


def datelist(start, end):  # (2014,4,5),(2014,5,7) => 2 days:{2014-04-05),(2014-05-06},(2014-05-07}
    # start_date = datetime.date(*start)
    start_date = start
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        if(int(curr_date.day)==1):
            result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
	t = 1	
	#while(t<31):
        curr_date += datetime.timedelta(1)
	#    t += 1
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result


if __name__ == '__main__':
    logging.info('start')

    #downloadPages(1, 100,sys.argv[0],sys.argv[0])
    #response = getPageInfo(url, 1, "2012-03-02","2012-04-01","四川省")
    #print response.content
    downloadPages("四川省")
    # "北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "上海市", "江苏省", "浙江省", "安徽省",
    # "福建省", "江西省", "山东省", "河南省", "湖北省",
    # "重庆市","广东省", "广西壮族自治区", "海南省", "四川省", "贵州省",
    #                "云南省", "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", "新疆维吾尔自治区高级人民法院生产建设兵团分院"

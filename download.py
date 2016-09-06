# -*- coding: utf-8 -*-
import sys
import re
import requests
import time
import urllib
def createTheForm(caseinfo):
    formid = 'DownloadForm'
    url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateListDocZip.aspx?action=1'
    form = {
        'id':formid,
        'conditions':'',
        'docIds':caseinfo,
        'keyCode':''
    }
    # r = requests.post(url=url,data=form)
    r2 = requests.get(url=url,params=form)
    return r2.url
    #print r.text

def downloadByFileName(fileName):

    source = open(r_name, 'r').read()

    # date
    dates1 = re.findall('裁判日期(.*?)案件名', source, re.S)
    dates = [da[5:-5] for da in dates1]

    names1 = re.findall('案件名称(.*?)文书ID', source, re.S)
    names = [na[5:-5] for na in names1]

    # doc_id
    doc_id1 = re.findall('文书ID(.*?)审判程序', source, re.S)
    doc_ids = [do[5:-5] for do in doc_id1]
    for (i, n, d) in zip(doc_ids, names, dates):
        info = i + "|" + n + "|" + d
        print info
        a = createTheForm(info)
        urllib.urlretrieve(a, './data/{}-{}-{}.txt'.format(i, n, d))
        time.sleep(3)  # 休眠1秒

if __name__ == '__main__':
    r_name = './page/ListContent'
    downloadByFileName(r_name)
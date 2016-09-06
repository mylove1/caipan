

import os

def getpageinfo():
    n = 1
    max_num = 1000
    url_source = 'wget  -P ./page http://wenshu.court.gov.cn/List/ListContent --post-data="Param=%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&Index={}&Page={}&Order=%E6%B3%95%E9%99%A2%E5%B1%82%E7%BA%A7&Direction=asc"'
    while(n<max_num):
        url = url_source.format(n,5)
        os.system(url)
        n = n + 1

if __name__ == '__main__':
    getpageinfo()

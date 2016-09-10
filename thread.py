# -*- coding: utf-8 -*-
import logging
from GetPageInfo_store import downloadPages
import threading
url = "http://wenshu.court.gov.cn/List/ListContent"
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

mylock = threading.RLock()
Page_Idx = 100
flag = True


class myThread(threading.Thread):
    def __init__(self, state):
        threading.Thread.__init__(self)
        self.state = state


    def run(self):
        logging.info('start')
        downloadPages(self.state)



if __name__ == '__main__':
    t = myThread("广东省")
    t.start()

    t1 = myThread("广西壮族自治区")
    t1.start()

    t2 = myThread("海南省")
    t2.start()

    t3 = myThread("四川省")
    t3.start()

    t4 = myThread("贵州省")
    t4.start()

    t5 = myThread("云南省")
    t5.start()

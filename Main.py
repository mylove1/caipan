# -*- coding: utf-8 -*-
import urllib
import os
import sys
import requests
import RandomHeader         #随机生成Header
# import PyV8
import  xml.dom as dom

reload(sys)
sys.setdefaultencoding("utf-8")

#全局变量
Test_file_url = 'D:\PythonTest'     #测试代码时放置文件的地方
Url = ["http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件"]

def test():
    form = {
        'Param':'案件类型:刑事案件',
        'index': 5,
        'Page':5,
        'Order':'法院层级',
        'Direction':'asc'
    }
    r = requests.get("http://wenshu.court.gov.cn/List/ListContent",params=form)
    print r.url
    # r = requests.post("http://wenshu.court.gov.cn/List/ListContent",data=form)
    # print r.url
    #print(r.text)
def test2(caseInfo):
    jscode = '''(
    function(caseInfo) {

        var formid = 'DownloadForm';
        var url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateListDocZip.aspx?action=1';
        var theform = document.createElement('form');
        theform.id = formid;
        theform.action = url;
        theform.method = 'POST';

        //获取检索条件，作为压缩包名称
        var $conditions = $(".removeCondtion");
        var conditions = "";
		if($conditions)
        $conditions.each(function () {
            conditions += $(this).attr("val") + "&";
        });
        conditions = conditions.substr(0, conditions.length - 1);
        conditions = conditions.replace(/:/g, "为").replace(/&/g, "且");

        var theInput = document.createElement('input');
        theInput.type = 'hidden';
        theInput.id = 'conditions';
        theInput.name = 'conditions';
        theInput.value = encodeURI(conditions);
        theform.appendChild(theInput);

        var theInput = document.createElement('input');
        theInput.type = 'hidden';
        theInput.id = 'docIds';
        theInput.name = 'docIds';
        theInput.value = caseInfo;
        theform.appendChild(theInput);

        //验证码功能暂未启用
        var theInput = document.createElement('input');
        theInput.type = 'hidden';
        theInput.id = 'keyCode';
        theInput.name = 'keyCode';
        theInput.value = '';
        theform.appendChild(theInput);

        theform.submit();
    }
    )'''
    class v8Doc(PyV8.JSClass):
        def write(self,s):
            print s.decode('utf-8')
        # def createElement(self,element):

    class Global(PyV8.JSClass):
        def __init__(self):
            self.document = v8Doc()
    ctxt = PyV8.JSContext(Global())
    ctxt.enter()
    DownLoadCase = ctxt.eval(jscode)
    DownLoadCase(caseInfo)
def js():
    class v8Doc(PyV8.JSClass):
        def write(self,s):
            print s.decode('utf-8')
    class Global(PyV8.JSClass):
        def __init__(self):
            self.document = v8Doc()
    ctxt = PyV8.JSContext(Global())
    ctxt.enter()
    hehefunc = ctxt.eval('''(
     function(name){
        name = name + " wan sui!"
        return name
     }

    )''')
    ctxt.eval("document.write('hehe');")
    print hehefunc("guoshen")


def getCaseInfo():
    caseinfo = ""
    return caseinfo
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


def createTheForm1():
    url = 'http://wenshu.court.gov.cn/List/ListContent'
    form = {
        'Param': '案件类型:刑事案件',
        'Index': 2,
        'Page': 5,
        'Order': '法院层级',
        'Direction': 'asc'
    }
    r2 = requests.get(url=url, params=form)
    print r2.url
    return r2.url

def test():
    # http: // wenshu.court.gov.cn / List / ListContent - -post - data = "Param=%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&Index=2&Page=5&Order=%E6%B3%95%E9%99%A2%E5%B1%82%E7%BA%A7&Direction=asc"
    n = 1
    url_source = 'wget http://wenshu.court.gov.cn/List/ListContent --post-data="Param=%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&Index={}&Page={}&Order=%E6%B3%95%E9%99%A2%E5%B1%82%E7%BA%A7&Direction=asc"'
    while(n<10):
        url = url_source.format(n,5)
        os.system(url)
        n = n + 1

if __name__ == '__main__':
    # print "Hello,World,I'm guoshen :)"
    # # js()
    # #test()
    # info2 = 'f08d44ee-b647-11e3-84e9-5cf3fc0c2c18|崔昌贵等贩卖、运输、制造毒品、杨林渠贩卖、制造毒品死刑复核刑事裁定书|2013-06-24'
    # info ='9aed51ab-f8b3-4f20-bf6e-06d8960c53d0|王某某合同诈骗指令再审决定书|2013-12-30'
    # info1 = 'f073d26d-b647-11e3-84e9-5cf3fc0c2c18|李良故意杀人死刑复核案刑事裁定书|2013-06-24'
    # # while(1):
    # #     caseinfo = getCaseInfo()
    # # a = createTheForm1()
    # a = createTheForm1()
    # urllib.urlretrieve(a, './2.html')
    import os
    file  = open('./page/record广东省.txt','w')
    file.write("page:10,date:2015-04-10")
    file.close()
    file = open('./page/record广东省.txt', 'r')
    source_ss = file.read()
    maps = source_ss.split(',')
    items = maps[0].split(':')
    items_date = maps[1].split(':')
    print items_date[1]


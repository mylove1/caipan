# -*- coding: utf-8 -*-

import os
import sys
import requests
import RandomHeader         #随机生成Header
try:
    import PyV8
except Exception:
    import pyv8
import  xml.dom as dom

reload(sys)
sys.setdefaultencoding("utf-8")

#全局变量
Test_file_url = './Files'     #测试代码时放置文件的地方
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
    caseinfo = info
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
    print r2.url
    #print r.text

if __name__ == '__main__':
    print "Hello,World,I'm the son of guoshen :)"
    # js()
    #test()
    info2 = 'f08d44ee-b647-11e3-84e9-5cf3fc0c2c18|崔昌贵等贩卖、运输、制造毒品、杨林渠贩卖、制造毒品死刑复核刑事裁定书|2013-06-24'
    info ='9aed51ab-f8b3-4f20-bf6e-06d8960c53d0|王某某合同诈骗指令再审决定书|2013-12-30'
    while(1):
        caseinfo = getCaseInfo()
        createTheForm(caseinfo)
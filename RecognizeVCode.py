# -*- coding: utf_8 -*-
import sys
import requests
import StringIO

reload(sys)
sys.setdefaultencoding("utf-8")

def crackVcode():

    url = 'http://wenshu.court.gov.cn/User/ValidateCode'

    headers = {
    'Host': 'wenshu.court.gov.cn',
    'Connection': 'keep-alive',
    'Cache-Control': "max-age=0",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Referer': 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cookie': 'ASP.NET_SessionId=3ks3gtwmyrfnqdsjmvetvqp5; wafenterurl=/List/List; wafcookie=a12defabf56a5562db7cb80c216203a4; __utma=61363882.568771455.1473331186.1473331186.1473331186.1; __utmc=61363882; __utmz=61363882.1473331186.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=aaazJcvVU--trcboOF5Bv; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1472542915,1472543876,1473311822,1473311827; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1473335174; _gscu_2116842793=71588436x2efq281; _gscs_2116842793=t73329792gshhbf12|pv:33; _gscbrs_2116842793=1; _gsref_2116842793=http://wenshu.court.gov.cn/'
    }

    response = requests.get(url=url, headers=headers)

    s = StringIO.StringIO()
    s.write(response.content)

    vcode = recognizeVCode(s)

    result = checkVcode(vcode)

    return vcode, result

def checkVcode(vcode):

    url = 'http://wenshu.court.gov.cn/Content/CheckVisitCode'

    data = {'ValidateCode': vcode}

    headers = {
    'Host': 'wenshu.court.gov.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Referer': 'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cookie': 'ASP.NET_SessionId=3ks3gtwmyrfnqdsjmvetvqp5; wafenterurl=/List/List; wafcookie=a12defabf56a5562db7cb80c216203a4; __utma=61363882.568771455.1473331186.1473331186.1473331186.1; __utmc=61363882; __utmz=61363882.1473331186.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=aaazJcvVU--trcboOF5Bv; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1472542915,1472543876,1473311822,1473311827; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1473335174; _gscu_2116842793=71588436x2efq281; _gscs_2116842793=t73329792gshhbf12|pv:33; _gscbrs_2116842793=1; _gsref_2116842793=http://wenshu.court.gov.cn/'
    }

    response = requests.post(url=url, data=data, headers=headers)

    return response.content

def recognizeVCode(picture_url):

    try:
        import pytesseract
        from PIL import Image
    except ImportError:
       print "导入失败！检查是否安装PIL or tesseract-ocr"

    image = Image.open(picture_url)
    vcode = pytesseract.image_to_string(image)
    return vcode

if  __name__== "__main__":
    #picture_url = 'ValidateCode.jpg'
    vcode, result = crackVcode()
    print vcode, 'result:', result


"""http://wenshu.court.gov.cn/waf_verify.htm"""
"""http://wenshu.court.gov.cn/waf_verify.htm?captcha=ews"""

"""http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html"""

"""http://wenshu.court.gov.cn/Content/CheckVisitCode
    post

    ValidateCode=415
"""
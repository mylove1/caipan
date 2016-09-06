# -*- coding: utf_8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

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
    picture_url = 'C:\Users\Hermit\PycharmProjects\China Judgement\ValidateCode1.jpg'
    vcode = recognizeVCode(picture_url)
    print vcode
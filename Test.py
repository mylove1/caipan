# -*- coding: utf_8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print 'fd'
    print 'http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil'
    print 'http://code.google.com/p/tesseract-ocr/'
    raise SystemExit

image = Image.open('./ValidateCode1.jpg')
vcode = pytesseract.image_to_string(image)
print vcode




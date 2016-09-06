# -*- coding: utf-8 -*-
import sys
import re
r_name = 'ListContent'
source = open(r_name, 'r').read()

# date

dates1 = re.findall('裁判日期(.*?)案件名',source,re.S)
print dates1
for da in dates1:
    print da[5:-5]

names1 = re.findall('案件名称(.*?)文书ID',source,re.S)
print names1
for na in names1:
    print na[5:-5]

# doc_id
doc_id1 = re.findall('文书ID(.*?)审判程序',source,re.S)
print doc_id1
for do in doc_id1:
    print do[5:-5]
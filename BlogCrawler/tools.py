#!/usr/bin/env python
# encoding: utf-8

"""
@author: puyangsky
@file: tools.py
@time: 2018/1/30 下午10:11
"""

import re


# 处理页面标签类
class Tool:
    def __init__(self):
        pass

    # 将代码剔除
    removeCode = re.compile('<code>.*?</code>', re.S)
    # 将超链接广告剔除
    removeADLink = re.compile('<div class="link_layer.*?</div>')
    # 去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    # 将多行空行删除
    removeNoneLine = re.compile('\n+')
    replaceGt = re.compile('&gt')
    replaceLt = re.compile('&lt')

    def replace(self, x):
        x = re.sub(self.removeCode, "", x)
        x = re.sub(self.removeADLink, "", x)
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = re.sub(self.removeNoneLine, "\n", x)
        x = re.sub(self.replaceGt, ">", x)
        x = re.sub(self.replaceLt, "<", x)
        # strip()将前后多余内容删除
        return x.strip()
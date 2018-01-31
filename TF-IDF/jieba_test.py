# -*- coding: utf-8 -*-

import jieba
import os
import jieba.analyse

file_path = "./test.txt"


def test():
    if os.path.exists(file_path):
        content = open(file_path, "r").read()
        print content
        tags = jieba.analyse.extract_tags(content, topK=20, withWeight=1)
        for tag in tags:
            print("tag: %s\t\t weight: %f" % (tag[0], tag[1]))


if __name__ == '__main__':
    test()
    # seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    # print("Full Mode: " + "/ ".join(seg_list))  # 全模式

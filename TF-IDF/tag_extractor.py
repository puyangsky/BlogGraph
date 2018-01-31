# -*- coding: utf-8 -*-

import jieba
import os
import jieba.analyse


class TagExtract:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.blog_dir = ""
        self.init_data_dir()

    def init_data_dir(self):
        cur_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_dir = os.path.join(cur_dir, "data")
        if os.path.exists(data_dir):
            self.blog_dir = os.path.join(data_dir, self.blog_name)

    def extract(self):
        if os.path.exists(self.blog_dir):
            for f in os.listdir(self.blog_dir):
                path = os.path.join(self.blog_dir, f)
                if not os.path.isfile(path):
                    continue
                content = open(path, "r").read()
                tags = jieba.analyse.extract_tags(content, topK=10, withWeight=1)
                print(path)
                for tag in tags:
                    print("tag: %s\t\t weight: %f" % (tag[0], tag[1]))


if __name__ == '__main__':
    tag_extract = TagExtract("puyangsky")
    tag_extract.extract()
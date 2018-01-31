# -*- coding: utf-8 -*-
from __future__ import print_function
import re

import requests
from lxml import etree
from tools import Tool
import os
import uuid


class Crawler:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.urls = set()
        self.hub_urls = set()
        self.blog_url = "http://www.cnblogs.com/"
        self.blog_dir = ""
        self.fetch_hub_url()
        self.parse_page_url()
        self.init_data_dir()

    @staticmethod
    def download(url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.content
        return ""

    def init_data_dir(self):
        cur_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_dir = os.path.join(cur_dir, "data")
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        self.blog_dir = os.path.join(data_dir, self.blog_name)
        if not os.path.exists(self.blog_dir):
            os.mkdir(self.blog_dir)

    def fetch_hub_url(self, page_url=None):
        """
        解析博客分页链接，将分页的所有链接填充到self.urls中
        """
        # 首页
        if page_url is None:
            page_url = self.blog_url + self.blog_name
            self.hub_urls.add(page_url)
        index_page = self.download(page_url)
        pagination = re.findall(".*<a href=\"(.*?)\">下一页</a>.*", index_page)
        if len(pagination) >= 1:
            page_url = pagination[0]
            self.hub_urls.add(page_url)
            # dfs
            return self.fetch_hub_url(page_url=page_url)
        else:
            # 到达末页
            self.hub_urls.add(page_url)
            return self.hub_urls

    def parse_page_url(self):
        """
        解析博客的所有文章链接，返回总数和链接列表
        :return:
        """
        if len(self.hub_urls) == 0:
            return
        for single_url in self.hub_urls:
            content = self.download(single_url)
            if content == "": continue
            html = etree.HTML(content)
            posts = html.xpath("//div[@class='postTitle']/a/@href")
            for post in posts:
                self.urls.add(post)
        print("Total urls size: %d" % len(self.urls))

    def dump_page_content(self, url, content):
        items = re.split('[/.]', url)
        if len(items) < 2:
            blog_id = str(uuid.uuid4())
        else:
            blog_id = items[-2]
        file_path = os.path.join(self.blog_dir, blog_id)
        with open(file_path, "w") as f:
            f.write(content)
        print("Dump one blog into %s" % file_path)

    def parse_single_page(self, url):
        """
        解析单个文章的内容，只取文章主体部分，作为主题生成的原材料
        """
        content = self.download(url)
        if content == "": return
        pattern = re.compile('<div id="cnblogs_post_body".*?>(.*?)</div>', re.S)
        match = pattern.search(content)
        if match:
            body = match.group(1)
            t = Tool()
            body = t.replace(body)
            self.dump_page_content(url, body)
        else:
            print("Parse page error")

    def parse_urls(self):
        for url in self.urls:
            self.parse_single_page(url)


if __name__ == '__main__':
    c = Crawler("puyangsky")
    c.parse_urls()

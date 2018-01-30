# -*- coding: utf-8 -*-
from __future__ import print_function
import re

import requests
from BlogCrawler import config
from lxml import etree


class Crawler:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.urls = set()
        self.hub_urls = set()
        # self.fetch_hub_url()
        # self.parse_page_url()

    @staticmethod
    def download(url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.content
        return ""

    def fetch_hub_url(self, page_url=None):
        """
        解析博客分页链接，将分页的所有链接填充到self.urls中
        """
        # 首页
        if page_url is None:
            page_url = config.BlogUrl + self.blog_name
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

    def parse_single_page(self, url):
        """
        解析单个文章的内容，只取文章主体部分，作为主题生成的原材料
        """
        content = self.download(url)
        if content == "": return
        # print(content)
        pattern = re.compile(r'<div id="cnblogs_post_body".*?>(.*?)</div>', re.M | re.X | re.U)
        match = pattern.search(content)
        if match:
            print(match.group(1))


if __name__ == '__main__':
    c = Crawler("puyangsky")
    c.parse_single_page("http://www.cnblogs.com/puyangsky/p/7545291.html")

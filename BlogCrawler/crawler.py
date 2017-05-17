# -*- coding: utf-8 -*-
import re

import requests
from BlogCrawler import config
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.urls = set([])

    @staticmethod
    def download(url):
        content = requests.get(url).content
        return content

    def parse_url(self, page_url=None):
        # 首页
        if page_url is None:
            page_url = config.BlogUrl + self.blog_name
            self.urls.add(page_url)
        index_page = self.download(page_url)
        # print index_page
        # html = BeautifulSoup(index_page, "lxml")
        # paginations = html.select('div[id="nav_next_page"] a')
        # paginations = html.find_all(re.compile("<a href=\"(.*?)\">下一页</a>"))
        # paginations = html.find_all("下一页")
        paginations = re.findall(".*<a href=\"(.*?)\">下一页</a>.*", index_page)
        if len(paginations) >= 1:
            page_url = paginations[0]
            self.urls.add(page_url)
            # dfs
            return self.parse_url(page_url=page_url)
        elif len(paginations) == 0:
            # 到达末页
            self.urls.add(page_url)
            return self.urls
        else:
            return []

    def test(self):
        page_url = "http://www.cnblogs.com/puyangsky/default.html?page=2"
        index_page = self.download(page_url)
        paginations = re.findall(".*<a href=\"(.*?)\">下一页</a>.*", index_page)
        if paginations:
            print paginations

    def parse_page_url(self):
        self.parse_url()
        if len(self.urls) == 0:
            return
        uid = 1
        page_urls = set([])
        for single_url in self.urls:
            page = self.download(single_url)
            html = BeautifulSoup(page, "lxml")
            posts = html.select('a[class="postTitle2"]')
            for post in posts:
                temp_url = post['href']
                page_urls.add(str(temp_url))
        for i in page_urls:
            # print str(uid) + "\t" + i
            uid += 1
        return uid, list(page_urls)

    def parse_single_page(self):
        page_count, page_urls = self.parse_page_url()
        if page_count == 0:
            return
        # for page_url in page_urls:
        page_url = page_urls[0]
        content = self.download(page_url)
        html = BeautifulSoup(content, "lxml")
        # print html.prettify()
        bodys = html.select('div[id="cnblogs_post_body"]')
        for body in bodys:
            print body
            # TODO 获取p、h1-h6


if __name__ == '__main__':
    c = Crawler("puyangsky")
    # urls = c.parse_url()
    # print urls
    c.parse_single_page()

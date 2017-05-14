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

    def parse_single_page(self):
        self.parse_url()
        if len(self.urls) == 0:
            print "Fuck"
            return
        print "Begin"
        id = 1
        post_urls = set([])
        for single_url in self.urls:
            page = self.download(single_url)
            html = BeautifulSoup(page, "lxml")
            posts = html.select('a[class="postTitle2"]')
            for post in posts:
                temp_url = post['href']
                post_urls.add(str(temp_url))
                print str(id) + "\t" + temp_url
                id += 1

if __name__ == '__main__':
    c = Crawler("puyangsky")
    # urls = c.parse_url()
    # print urls
    c.parse_single_page()
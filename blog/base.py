#!/user/bin/env python
# coding=utf-8
'''
@project : blog-auto-sender
@author  : song.yilong
#@ide    : PyCharm
#@time   : 2020-03-30 11:48:51
'''
from selenium.webdriver.support.wait import WebDriverWait


class BaseBlog(object):

    def __init__(self, driver, timeout = 10):
        self.driver = driver
        self.timeout = timeout

    def parse_contents(self, contents: dict):
        self.title = contents.get("title") or "unknown"
        self.content = contents.get("content") or "..."
        self.summary = contents.get("summary") or "..."
        self.name = contents.get("name") # 文章别名
        self.categories = contents.get("categories") or []
        self.tags = contents.get("tags") or []
        self.author = contents.get("author")
        self.cover = contents.get("cover")
        self.blog = contents.get("blog") or "https://blog.yilon.top"
        self.csdn_category = contents.get("csdn_category") or "原创"
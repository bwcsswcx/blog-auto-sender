#!/user/bin/env python
# coding=utf-8
'''
@project : blog-auto-sender
@author  : song.yilong
#@ide    : PyCharm
#@time   : 2020-03-30 21:09:27
'''
import time

from selenium.webdriver.support.wait import WebDriverWait

from blog.base import BaseBlog

from selenium.webdriver.firefox.webdriver import WebDriver #todo

class CDBLOG(BaseBlog):

    login_path = "https://account.cnblogs.com/signin?returnUrl=https%3A%2F%2Fi-beta.cnblogs.com%2Fposts%2Fedit"

    def __init__(self, driver : WebDriver, config, timeout, contents: dict):
        super().__init__(driver, timeout)
        self.driver = driver

        self.config = config
        self.contents = contents

        self.parse_config(config)
        self.parse_contents(contents)
        self.do_assert()


    def parse_config(self, config):
        blog_cfg = (config.get("blog") or dict()).get("cnblog") or dict()
        login_cfg = blog_cfg.get("login") or dict()
        self.username = login_cfg.get("username")
        self.password = login_cfg.get("password")

    def do_assert(self):
        assert self.username and self.password, "请输入用户名或密码"
        assert self.title and self.content, "请输入文章标题或内容"

    def login_(self):
        self.driver.get(url=self.login_path)

        button = self.driver.find_element_by_xpath("//button[@id='submitBtn']")
        self.driver.find_element_by_xpath("//input[@name='LoginName']").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name='Password']").send_keys(self.password)
        button.submit()
        time.sleep(1)
        button.submit()
        self.driver.get_cookies()
        time.sleep(3)

    def write_blog(self):
        print(self.driver.title)
        # 标题
        self.driver.switch_to.default_content()
        title = WebDriverWait(self.driver, self.timeout).until(lambda x : x.find_element_by_id("post-title"))
        title.clear()
        title.send_keys(self.title)

        # 正文
        editer = self.driver.find_element_by_id("md-editor")
        editer.clear()
        editer.send_keys(self.content)

        # 发布
        button = self.driver.find_element_by_xpath("//button[@cnbellocator='publishBtn']")
        button.click()

    def do_handler(self):
        # 1. 登陆
        self.login_()
        self.write_blog()


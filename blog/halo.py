#!/user/bin/env python
# coding=utf-8
'''
@project : blog-auto-sender
@author  : song.yilong
#@ide    : PyCharm
#@time   : 2020-03-29 21:20:48
'''
import time

import pykeyboard
import pyperclip
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from blog.base import BaseBlog


class Halo(BaseBlog):
    dashboard_path = "https://blog.yilon.top/admin/index.html"
    write_path = "https://blog.yilon.top/admin/index.html#/posts/write"

    def __init__(self, driver, config, timeout, contents: dict):
        super().__init__(driver, timeout)
        self.driver = driver

        self.config = config
        self.contents = contents

        self.parse_config(config)
        self.parse_contents(contents)
        self.do_assert()

    def parse_config(self, config):
        blog_cfg = (config.get("blog") or dict()).get("halo") or dict()
        login_cfg = blog_cfg.get("login") or dict()
        self.username = login_cfg.get("username")
        self.password = login_cfg.get("password")

    def do_assert(self):
        assert self.username and self.password, "请输入用户名或密码"
        assert self.title and self.content, "请输入文章标题或内容"

    def login_(self):
        """登陆后台"""

        # 打开页面
        self.driver.get(self.dashboard_path)
        self.driver.maximize_window()

        # 设置用户名和密码
        form_ele = self.driver.find_element_by_class_name("login-form.animated")
        username_ele, password_ele = form_ele.find_elements_by_class_name("ant-input")
        username_ele.clear()
        username_ele.send_keys(self.username)
        password_ele.clear()
        password_ele.send_keys(self.password)
        # 点击提交按钮
        button = self.driver.find_element_by_xpath("//button[@type='button']")
        button.click()

    def open_write_page(self):
        """
        打开写新文章页面
        :return:
        """
        # 查找头部元素
        e_header = WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_class_name("router-link-exact-active.router-link-active"))

        # 查找文章页
        e_headers = e_header.find_elements_by_xpath("//ul/li/div")
        e_article = e_headers[0]
        for x in e_headers:
            if "文章" == x.text:
                e_article = x
                break
        ActionChains(self.driver).move_to_element(e_article).perform()
        # 上面花里胡哨得都没用
        self.driver.get(self.write_path)

    def write_blog(self):
        # 写入文章标题
        ele_title = WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_xpath("//*[@placeholder='请输入文章标题']"))
        ele_title.clear()
        ele_title.send_keys(self.title)
        # 写入文章正文
        ele_edit = WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_xpath("//textarea[@placeholder='开始编辑...']"))
        ele_edit.clear()
        ele_edit.click()
        # 由于某些编辑器对输入有自动格式化，可通过模拟复制粘贴的方式解决
        # ele_edit.send_keys(self.content)
        pyperclip.copy(self.content)
        k = pykeyboard.PyKeyboard()

        ele_edit.send_keys(Keys.CONTROL, 'a')
        ele_edit.send_keys(Keys.RETURN)
        time.sleep(1)
        # ele_edit.send_keys(Keys.CONTROL, 'v')
        k.press_keys(['Command', 'v'])
        k.press_keys(['Return'])
        time.sleep(1)

        # 点击发布按钮
        ele_publish = self.driver.find_element_by_class_name("ant-pro-footer-toolbar").find_element_by_xpath(
            "//button[@class='ant-btn ant-btn-primary']")
        ele_publish.click()

    def __add_new_categories(self, new_categories):
        if not new_categories: return
        ele_from = self.driver.find_element_by_xpath('//form[@class="ant-form ant-form-vertical"]')
        # 点击添加按钮
        button = ele_from.find_element_by_xpath(
            "//span[@class='ant-form-item-children']/button[@class='ant-btn ant-btn-dashed']")
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        ActionChains(self.driver).move_to_element(button).click().perform()
        # 设置分类值
        category = WebDriverWait(ele_from, self.timeout).until(
            lambda x: x.find_element_by_xpath("//input[@placeholder='分类名称']"))
        category.clear()
        category.send_keys(new_categories[0])
        # 点击保存按钮
        buttons = ele_from.find_elements_by_xpath("//button[@class='ant-btn ant-btn-primary']")
        for button in buttons:
            if "保 存" == button.text:
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                ActionChains(self.driver).move_to_element(button).click().perform()

    def __get_new_categories(self):
        ele_from = self.driver.find_element_by_xpath('//form[@class="ant-form ant-form-vertical"]')
        lis_ = ele_from.find_elements_by_xpath(
            "//ul[@class='ant-tree ant-tree-icon-hide']/li/span[@class='ant-tree-node-content-wrapper ant-tree-node-content-wrapper-normal']")
        added_categories = [x.get_attribute("title") for x in lis_]
        new_categories = [x for x in self.categories if x not in added_categories]
        return new_categories

    def __select_category(self):
        ele_from = self.driver.find_element_by_xpath('//form[@class="ant-form ant-form-vertical"]')
        for category in self.categories:
            li_ = WebDriverWait(ele_from, self.timeout).until(lambda x: x.find_element_by_xpath(
                "//ul[@class='ant-tree ant-tree-icon-hide']/li/span[@class='ant-tree-node-content-wrapper ant-tree-node-content-wrapper-normal'][@title='{category}']".format(
                    category=category)))
            checkbox = li_.find_element_by_xpath("../span[@class='ant-tree-checkbox']")
            self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            ActionChains(self.driver).move_to_element(checkbox).click().perform()

    def __select_tags(self):
        if not self.tags: return
        # 找到tag位置并且点击
        e_tag = self.driver.find_element_by_xpath(
            "//form[@class='ant-form ant-form-vertical']//div[@class='ant-select ant-select-enabled ant-select-allow-clear']")
        e_tag = e_tag.find_element_by_xpath("//input[@class='ant-select-search__field']")
        self.driver.execute_script("arguments[0].scrollIntoView();", e_tag)
        ActionChains(self.driver).move_to_element(e_tag).click().perform()

        time.sleep(0.5)
        for tag in self.tags:
            e_tag.send_keys(tag)
            time.sleep(0.5)
            e_tag.send_keys(Keys.RETURN)
            time.sleep(0.5)

    def __write_categories(self):
        if not self.categories: return
        # 计算需要新增的分类
        new_categories = self.__get_new_categories()
        # 添加新分类
        self.__add_new_categories(new_categories)
        # 选择分类
        self.__select_category()

    def write_publish(self):
        # ---------------填写基本设置---------------
        basic = WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_xpath("//form[@class='ant-form ant-form-vertical']"))
        # 名称
        if self.name:
            name = basic.find_element_by_xpath("//input[@class='ant-input']")
            name.clear()
            name.send_keys(self.name)
        # ---------------填写分类---------------
        self.__write_categories()
        # ---------------选择标签---------------
        self.__select_tags()
        # ---------------填写摘要---------------
        if self.summary:
            ele_summary = self.driver.find_element_by_xpath("//textarea[@placeholder='如不填写，会从文章中自动截取']")
            ele_summary.send_keys(self.summary)
        # ---------------封面图---------------
        if self.cover:
            ele_cover = self.driver.find_element_by_xpath("//input[@placeholder='点击封面图选择图片，或者输入外部链接']")
            ele_cover.send_keys(self.cover)

    def publish(self):
        button = self.driver.find_element_by_xpath("//div[@class='bottom-control']/button[3]")
        button.click()

    def do_handler(self):
        # 登陆
        self.login_()
        # 打开编辑页
        self.open_write_page()
        # 写文章
        self.write_blog()
        # 填写发布信息
        self.write_publish()
        # 发布
        self.publish()

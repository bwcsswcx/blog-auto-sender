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
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from blog import authorize
from blog.base import BaseBlog


class CSDN(BaseBlog):
    login = 'https://passport.csdn.net/login?code=public'

    def __init__(self, driver, config, timeout, contents: dict):
        super().__init__(driver, timeout)
        self.driver = driver

        self.config = config
        self.contents = contents

        self.parse_config(config)
        self.parse_contents(contents)
        self.do_assert()

    def parse_config(self, config):
        pass

    def do_assert(self):
        assert self.title and self.content, "请输入文章标题或内容"

    def login_(self):
        # 使用qq登陆，密码验证有拖动条，没有此方便
        # 1. 跳转登陆
        self.driver.get(self.login)
        # 2.窗口最大化
        self.driver.maximize_window()
        # 4.使用QQ授权登录
        self.driver.find_element_by_link_text('社交账号登录').click()
        self.driver.find_element_by_xpath("//li[@class='icon-list']/a[@class='icon-qq']").click()
        self.driver.close()
        authorize.qq(self.driver, self.timeout)

    def open_write_page(self):
        # 1.点击"写博客"
        self.driver.switch_to.default_content()  # 退出frame，没有这一句后续的元素定位会出错
        write_blog = WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_element_by_xpath("/html/body/div[1]/div/div/ul/li[@class='write-bolg-btn']/a"))
        write_blog.click()
        self.driver.close()
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])

        # 2.点击"内容发布"
        start = WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_link_text("内容发布"))
        start.click()

        # 3.点击"Markdown编辑器"
        md_c = WebDriverWait(self.driver, self.timeout).until(
            lambda x: x.find_element_by_link_text("Markdown编辑器"))
        md_c.click()


    def write_blog(self):
        self.driver.close()
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])
        # 1. 输入文章标题
        title = WebDriverWait(self.driver, self.timeout).until(lambda x : x.find_element_by_xpath("//input[@class='article-bar__title article-bar__title--input text-input']"))
        ActionChains(self.driver).click(title).perform()
        title.clear()
        title.send_keys(Keys.CONTROL, 'a')
        title.send_keys(Keys.DELETE)
        title.send_keys(self.title)
        # PS:下面这行代码很重要，卡了好久才解决┭┮﹏┭┮，不信可以试试注释掉这句

        # 2.输入正文 通过键盘事件解决
        editor = self.driver.find_element_by_xpath("//div[@class='cledit-section']")
        ActionChains(self.driver).click(editor).perform()
        pyperclip.copy(self.content)
        k = pykeyboard.PyKeyboard()
        time.sleep(1)
        k.press_keys(['Command', 'a'])
        k.press_keys(['Return'])
        time.sleep(0.5)
        k.press_keys(['Command', 'v'])
        k.press_keys(['Return'])
        time.sleep(2)

        # 3. 发布文章按钮
        self.driver.find_element_by_xpath("//div[@class='article-bar__user-box flex flex--row']/button[@class='btn btn-publish']").click()

    def publish_(self):
        # 1. 添加标签
        add_tag = WebDriverWait(self.driver, self.timeout).until(lambda d: d.find_element_by_xpath('//div[@class="mark_selection_title_el_tag"]'))
        add_tag.click()
        tag_input = WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.find_element_by_xpath('//input[@class="el-input__inner"]'))
        tag_input.clear()
        tag_input.click()
        time.sleep(1)
        for i, tag in enumerate(self.tags):
            tag_input.send_keys(tag, Keys.RETURN)
            time.sleep(1)
        self.driver.find_element_by_xpath("//button[@class='modal__close-button button']").click()


        # 2.添加分类
        category = WebDriverWait(self.driver, self.timeout).until(lambda d: d.find_element_by_xpath('//button[@class="tag__btn-tag"]'))
        ActionChains(self.driver).move_to_element(category).click().perform()

        # 3.模拟键盘输入即可
        k = pykeyboard.PyKeyboard()
        ActionChains(self.driver).click(category).perform()
        k.press_keys(['Return'])
        for category in self.categories:
            pyperclip.copy(category)
            time.sleep(1)
            k.press_keys(['Command', 'v'])
            k.press_keys(['Return'])
            time.sleep(2)
        # 4. 文章类型
        select = Select(self.driver.find_element_by_xpath("//div[@class='form-entry__field']/select[@class='textfield']"))
        print(self.csdn_category)
        select.select_by_visible_text(self.csdn_category)

        # 5.发布
        button = self.driver.find_element_by_xpath("//div[@class='modal__button-bar']/button[@class='button btn-b-red']")
        button.click()

    def do_handler(self):
        # 登陆
        self.login_()
        # 打开编辑页面
        self.open_write_page()
        # 写文章
        self.write_blog()
        # 发布文章
        self.publish_()




#!/user/bin/env python
# coding=utf-8
'''
@project : blog-auto-sender
@author  : song.yilong
#@ide    : PyCharm
#@time   : 2020-03-29 16:40:50
'''

from selenium.webdriver.support.wait import WebDriverWait


# QQ授权登录, 使用前提是QQ客户端在线
def qq(driver, timeout):
    # 切换到最新打开的窗口
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    print('qq authorize title is ', driver.title)

    # 切换iframe
    iframe = WebDriverWait(driver, timeout).until(lambda d: d.find_element_by_id('ptlogin_iframe'))
    driver.switch_to.frame(iframe)

    # 点击头像进行授权登录
    login = WebDriverWait(driver, timeout).until(lambda d: d.find_element_by_xpath('//*[@id="qlogin_list"]/a[1]'))
    login.click()
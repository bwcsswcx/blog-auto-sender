#!/user/bin/env python
# coding=utf-8
'''
@project : blog-auto-sender
@author  : song.yilong
#@ide    : PyCharm
#@time   : 2020-03-29 16:40:05
'''
import datetime
import sys
import time

import yaml
from selenium import webdriver


from blog import halo, csdn, cnblog


def load_config():
    with open("config.yaml", "r", encoding='UTF-8') as fr:
        return yaml.load(fr, Loader=yaml.FullLoader)

def get_driver(config):
    driver = config.get("driver")
    return getattr(webdriver, driver.get("type"))(executable_path=driver.get("path"))


def parse_md(file_path):
    contents = dict()
    with open(file_path, 'r', encoding='UTF-8') as fr:
        file = fr.read()
        fields = file.split("---")
        yamls = yaml.load(fields[1].strip(), Loader=yaml.FullLoader)
        contents.update(yamls)
        contents["content"] = "\r\n".join(file.split("---\n```")[1:])
    return contents


def post_halo(driver, config, timeout, contents):
    start_time = datetime.datetime.now()
    try:
        print(datetime.datetime.now(), "开始发布个人博客...")
        halo.Halo(driver, config, timeout, contents).do_handler()
        print(datetime.datetime.now(), "个人博客发布完成！cost:", (datetime.datetime.now()-start_time).seconds)
    finally:
        time.sleep(3)
        driver.close()


def post_csdn(driver, config, timeout, contents):
    start_time = datetime.datetime.now()
    try:
        print(datetime.datetime.now(), "开始发布CSDN...")
        csdn.CSDN(driver, config, timeout, contents).do_handler()
        print(datetime.datetime.now(), "CSDN发布完成！cost:", (datetime.datetime.now() - start_time).seconds)
    finally:
        time.sleep(3)
        driver.close()


def post_cnblog(driver, config, timeout, contents):
    start_time = datetime.datetime.now()
    try:
        print(datetime.datetime.now(), "开始发布博客园...")
        cnblog.CDBLOG(driver, config, timeout, contents).do_handler()
        print(datetime.datetime.now(), "博客园发布完成！cost:", (datetime.datetime.now() - start_time).seconds)
    finally:
        time.sleep(3)
        driver.close()


timeout = 13 # 单位：秒
config = load_config()
# 解析文章内容
assert len(sys.argv) > 1, "请输入文件全路径"
contents = parse_md(sys.argv[1])
# 发布个人博客

# 简单界面式
while True:
    print("\n\n此发布系统支持以下平台，请选择:")
    print("--- 1. halo 个人博客 ---")
    print("--- 2. csdn 博客    ---")
    print("--- 3. 博客园       ---")
    print("--- 0. 退出         ---")
    choise = input("-->")
    if choise not in ["0", "1", "2", "3"]:
        print("输入有误，重新输入。")
        time.sleep(3)
        continue

    # 加载驱动
    driver = get_driver(config)
    if "0" == choise:
        break
    if "1" == choise:
        post_halo(driver, config, timeout, contents)
        continue
    if "2" == choise:
        post_csdn(driver, config, timeout, contents)
        continue
    if "3" == choise:
        post_cnblog(driver, config, timeout, contents)
        continue

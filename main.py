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
        contents["content"] = ""
        if contents.get("blog"):
            contents["content"] += "\n" + "> **Blog: https://blog.yilon.top**"
        contents["content"] += "\r\n".join(file.split("---\n```")[1:])
        if contents.get("blog"):
            contents["content"] += "\n" + "> **Blog: https://blog.yilon.top**"
    return contents


def post_halo(config, timeout, contents):
    driver = get_driver(config)
    start_time = datetime.datetime.now()
    try:
        print(datetime.datetime.now(), "开始发布个人博客...")
        halo.Halo(driver, config, timeout, contents).do_handler()
        print(datetime.datetime.now(), "个人博客发布完成！cost:", (datetime.datetime.now()-start_time).seconds)
    finally:
        driver.close()


def post_csdn(config, timeout, contents):
    driver = get_driver(config)
    start_time = datetime.datetime.now()
    try:
        print(datetime.datetime.now(), "开始发布CSDN...")
        csdn.CSDN(driver, config, timeout, contents).do_handler()
        print(datetime.datetime.now(), "CSDN发布完成！cost:", (datetime.datetime.now() - start_time).seconds)
    finally:
        driver.close()


def post_cnblog(config, timeout, contents):
    driver = get_driver(config)
    start_time = datetime.datetime.now()
    try:
        print(datetime.datetime.now(), "开始发布博客园...")
        cnblog.CDBLOG(driver, config, timeout, contents).do_handler()
        print(datetime.datetime.now(), "博客园发布完成！cost:", (datetime.datetime.now() - start_time).seconds)
    finally:
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
    if "0" == choise:
        break
    if "1" == choise:
        post_halo(config, timeout, contents)
        continue
    if "2" == choise:
        post_csdn(config, timeout, contents)
        continue
    if "3" == choise:
        post_cnblog(config, timeout, contents)
        continue

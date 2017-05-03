#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description :

import os
from selenium import webdriver
from time import sleep
import hashlib
import string
from screenshot_log import *
from screenshot_config import *
from PIL import Image
import requests


def md5encode(str):
    m = hashlib.md5()
    m.update(str.encode(encoding='utf-8'))
    return m.hexdigest()

# def initialize_mkdir():
#    # 初始化存储目录.不存在则新建目录
#    for i in string.hexdigits[:16]:
#        dirs = SCREENSHOT_DIR + '/' + str(i)
#        if not os.path.exists(dirs):
#            os.makedirs(dirs)


def initialize_mkdir():
    # 初始化存储目录.不存在则新建目录
    for i in string.hexdigits[:16]:
        for j in string.hexdigits[:16]:
            dirs = SCREENSHOT_DIR + '/' + str(i) + str(j)
#            print(dirs)
            if not os.path.exists(dirs):
                os.makedirs(dirs)


def png2jpg(pwd):
    try:
        im = Image.open(pwd)
        im.save(pwd, "JPEG")
        return True
    except Exception as e:
        logging.error('error {}'.format(e))
        return False


def pic_scale(pwd):
    # 如果宽度大于300,统一等比例缩放到300宽度
    try:
        im = Image.open(pwd)
        # 获得图像尺寸:
        w, h = im.size
#        print('Original image size: %sx%s' % (w, h))
        if w > 300:
            proportion = w / 300
            after_w = 300
            after_h = h // proportion

        # 缩放按比例缩放
        im.thumbnail((w // proportion, h // proportion))
#        print('Resize image to: %sx%s' % (w//proportion, h//proportion))
        # 把缩放后的图像用png格式保存
        after_pwd = pwd.split('.')[0] + '.png'
#        print(after_pwd)
        im.save(after_pwd, 'png')
        return True
    except Exception as e:
        logging.error('error {}'.format(e))
        return False


def verify_respone(url):
    try:
        if requests.head(url, timeout=TIMEOUT).status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        logging.error('error {}'.format(e))
        return False


def screenshots(url, cut):
    try:
        browser = webdriver.PhantomJS()

        width = cut.split(",")[0]
        height = cut.split(",")[1]
        x = cut.split(",")[2]
        y = cut.split(",")[3]

        save_dir = SCREENSHOT_DIR + '/' + str(md5encode(url))[0:2]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_pwd = save_dir + '/' + str(md5encode(url)) + '.png'

        if verify_respone(url):
            browser.set_window_position(x, y)
            browser.set_window_size(width, height)
            browser.set_page_load_timeout(TIMEOUT)
            browser.get(url)
#            print(url,save_pwd)

            # 设置背景色为白色否则截图会有透明颜色,必须在browser.get(url)后设置才生效
            browser.execute_script('document.body.style.background = "white"')
            browser.save_screenshot(save_pwd)
            browser.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    initialize_log()
    initialize_mkdir()
#    print(md5Encode('www.baidu.com'))
#    pic_scale('/data0/moosefs/client/screenshots/09/0941db86572a3ce150e56fa744ea82fb.png')
#    pic_scale('/data0/moosefs/client/screenshots/12/12c4463efca56848976685b419d7a313.png')
#    print(verify_respone('http://www.baidu.com'))

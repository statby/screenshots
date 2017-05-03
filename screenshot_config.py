#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description : 配置文件


LOGFILEDIR = '/opt/screenshots/logs/screenshot.log'
PIDFILE = '/tmp/screenshot_daemon.pid'
STDOUTLOG = '/opt/screenshots/logs/screenshot_stdout.log'
STDERRLOG = '/opt/screenshots/logs/screenshot_stderr.log'
# SCREENSHOT_DIR='/root/development/screenshot/screens'
SCREENSHOT_DIR = '/data0/moosefs/client/screenshots'
TIMEOUT = 10

# scribe config
IS_SCRIBE = False      # 是否开启scribe远程打日志,True|False
SCRIBE_HOST = '192.168.10.206'
SCRIBE_PORT = '1463'
SCRIBE_CATEGORY = 'screenshot'

HOSTNAME = 'screenshot'


# redis config
redis_host = 'localhost'
redis_port = 6379
redis_db = 0


# public config
IS_SCALE = True     # 是否开启等比例压缩,如果图片宽度大于300,等比例压缩至宽度为300  True|False

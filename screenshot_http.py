#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description :

from flask import Flask, request
from screenshots import *
from screenshot_redis import *
from screenshot_log import *
from screenshot_config import *


app = Flask(__name__)


@app.route('/screenshot', methods=['POST', 'GET'])
def screenshot():
    screen_redis = ConnectRedis()
    screen_redis = screen_redis.redis_class()
#    print(request.headers)
#    print(request.headers['Content-Type'])
    if request.headers['Content-Type'] == 'application/json':
        post_list = request.json['lists']
        try:
            for post_lists in post_list:
                screen_redis.lpush('screenshot_queue', str(post_lists))
                logging.info("lpush {}".format(post_lists))
            return 'ok'
        except Exception as e:
            logging.error("error {}".format(e))
            return 'error'
    else:
        try:
            url = request.values.get("url")
            cut = request.values.get("cut")
            if cut is None:
                cut = '1920,1080,0,0'
#             print("url:", url, type(url))
#             print("cut:", cut, type(cut))
            if url and cut:
                if screenshots(url, cut):
                    return 'ok'
                else:
                    return 'error'
        except Exception as e:
            logging.error("error {}".format(e))
            return 'error'


if __name__ == '__main__':
    initialize_log()
    app.run(host='0.0.0.0', port=2222, debug=False)

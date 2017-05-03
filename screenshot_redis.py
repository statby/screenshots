#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description :


import redis
from screenshot_config import *


class ConnectRedis:

    def __init__(self):
        self.r = redis.StrictRedis(
            host=redis_host, port=redis_port, db=redis_db)

    def redis_class(self):
        return self.r

    def hlen(self, key):
        return self.r.hlen(key)

    def lpush(self, *keys):
        try:
            if self.r.lpush(*keys):
                return True
            else:
                return False
        except Exception as e:
            print(e)


if __name__ == '__main__':

    test = ConnectRedis()
    print(test.hlen('aaa'))

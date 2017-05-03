#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description :


import os
import sys
import logging
from screenshot_config import *


def initialize_log():
    LOGDIR = '/'.join(LOGFILEDIR.split('/')[0:-1])

    if sys.version_info[0] == 2:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    if os.path.exists(LOGDIR):
        pass
    else:
        os.makedirs(LOGDIR)

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s %(name)s %(funcName)s %(lineno)d',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filename=LOGFILEDIR,
                        level=logging.INFO,
                        )


if __name__ == '__main__':
    initialize_log()
    logging.debug("debug message")
    logging.info("info message")
    logging.warn("warn message")
    logging.error("error message")
    logging.critical("critical message")

#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description :


from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from screenshot_config import *
from screenshot_log import *


def screenshot_scribe(msg):
    try:
        socket = TSocket.TSocket(host=SCRIBE_HOST, port=SCRIBE_PORT)
        transport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(
            trans=transport, strictRead=False, strictWrite=False)
        client = scribe.Client(protocol)
        transport.open()

        category = SCRIBE_CATEGORY
        log_entry = scribe.LogEntry(category, msg)
        result = client.Log(messages=[log_entry])
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        logging.error(e)
        return False


if __name__ == '__main__':
    screenshot_scribe(
        '2017-04-24 23:48:36screenshotscreenshot151200.0.0.0')

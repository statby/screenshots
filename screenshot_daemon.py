#!/bin/env python3
# coding=utf-8
# Author      : Statby
# Description : 配置文件

import os
import sys
import time
import atexit
import signal
from screenshot_redis import *
from screenshots import *
from screenshot_log import *
from screenshot_config import *
from screenshot_scribe import *


def daemonize(pidfile, *, stdin='/dev/null',
              stdout='/dev/null',
              stderr='/dev/null'):

    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)   # Parent exit
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork (relinquish session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)

    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))

    # Signal handler for termination (required)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


def conn_redis():
    screen - ConnectRedis()
    screen_redis = screen.redis_class()
    llen = screen_redis.llen('unscreenshot')
    return llen


def ntime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def retry_screenshot():
    try:
        screen = ConnectRedis()
        screen_redis = screen.redis_class()
        processing_url = screen_redis.lpop('screenshot_fail_queue')
        if processing_url:
            processing = eval(processing_url.decode())
            url = processing['url']
            cut = processing['cut']
            retry = processing['retry']
            save_pwd = SCREENSHOT_DIR + '/' + \
                str(md5encode(url))[0:2] + '/' + str(md5encode(url)) + '.png'
            if retry < 3:
                if screenshots(url, cut):
                    processing['time'] = ntime()
                    processing['pwd'] = save_pwd
                    finish = processing
                    logging.info('finish retry screenshots {}'.format(finish))
                else:
                    processing['time'] = ntime()
                    processing['pwd'] = save_pwd
                    processing['retry'] += 1
                    finish = processing
                    screen_redis.lpush('screenshot_fail_queue', str(finish))
                    logging.error('fail retry screenshot {} '.format(finish))
            else:
                processing['time'] = ntime()
                processing['pwd'] = save_pwd
                finish = processing
                key = url + '?' + str(int(time.time()))
                screen_redis.hset('screenshot_fail', key, str(finish))
                logging.error(
                    'fail retry screenshot,move to screenshot_fail {} '.format(finish))
        else:
            pass
    except Exception as e:
        logging.error(e)


def main():
    #    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    logging.info('info Daemon started with pid {}\n'.format(os.getpid()))

    while True:
        time.sleep(1)
        screen = ConnectRedis()
        screen_redis = screen.redis_class()
        processing_url = screen_redis.lpop('screenshot_queue')

        if processing_url:
            try:
                processing = eval(processing_url.decode())
                url = processing['url']
                cut = processing['cut']
                save_pwd = SCREENSHOT_DIR + '/' + \
                    str(md5encode(url))[0:2] + '/' + \
                    str(md5encode(url)) + '.png'
                before_time = time.time()
                if screenshots(url, cut):
                    try:
                        after_time = time.time()
                        runtime = str(int((after_time - before_time) * 1000))
                        source = '0.0.0.0'
                        scribe_msg = '\01'.join(
                            [str(ntime()), HOSTNAME, SCRIBE_CATEGORY, runtime, '0', source])
                        if IS_SCRIBE:
                            screenshot_scribe(scribe_msg)
                        else:
                            pass
                    except Exception as e:
                        logging.error('scribe fail {}'.format(e))
                        pass

                    processing['time'] = ntime()
                    processing['pwd'] = save_pwd
                    finish = processing
                    key = url + '?' + str(int(time.time()))
                    screen_redis.hset('screenshot_ok', key, str(finish))
                    logging.info('finish screenshots {}'.format(finish))
                    width = int(cut.split(",")[0])

                    if IS_SCALE:
                        try:
                            # 如果图片宽度大于300,等比例压缩至300
                            if width > 300:
                                height = int(cut.split(",")[1])
                                proportion = width / 300
                                scale_width = width // proportion
                                scale_height = height // proportion
                                x = cut.split(",")[2]
                                y = cut.split(",")[3]
                                cut = str(int(scale_width)) + ',' + \
                                    str(int(scale_height)) + ',' + x + ',' + y
                                finish['cut'] = cut
                                if pic_scale(save_pwd):
                                    logging.info(
                                        'finish pic_scale {}'.format(finish))
                                else:
                                    logging.error(
                                        'fail pic_scale {}'.format(finish))
                        except Exception as e:
                            logging.error('error {}'.format(e))
                    else:
                        pass

#                    if png2jpg(save_pwd):
#                        logging.info('info finish png2jpg {}'.format(finish))
#                    else:
#                        logging.error('error png2jpg {}'.format(finish))
#                    screen_redis.lpush('screenshot_ok',str(finish))

                else:
                    processing['time'] = ntime()
                    processing['pwd'] = save_pwd
                    processing['retry'] = 0
                    finish = processing
                    screen_redis.lpush('screenshot_fail_queue', str(finish))
                    logging.error(
                        'fail screenshot,move to screenshot_fail_queue {} '.format(finish))

            except Exception as e:
                #                sys.stdout.write('{} {}'.format(time.ctime(),e))
                logging.error('error {} {}'.format(time.ctime(), e))

        # 截图失败尝试重试三次的功能
        retry_screenshot()


def start():
    try:
        daemonize(PIDFILE,
                  stdout=STDOUTLOG,
                  stderr=STDERRLOG)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
    main()


def stop():
    if os.path.exists(PIDFILE):
        with open(PIDFILE) as f:
            os.kill(int(f.read()), signal.SIGTERM)
    else:
        print('Not running', file=sys.stderr)
#        raise SystemExit(1)


if __name__ == '__main__':
    initialize_log()
#    retry_screenshot()

    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    if sys.argv[1] == 'start':
        start()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'restart':
        if os.path.exists(PIDFILE):
            with open(PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
                sys.stdout.write('{} service stop\n'.format(time.ctime()))
                start()
        else:
            start()
            sys.stdout.write('{} service start\n'.format(time.ctime()))
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)

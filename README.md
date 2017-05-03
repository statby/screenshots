##微服务screenshots说明档

- 微服务名:  screenshots
- Python3 + Flask + Selenium + PhantomJS http screenshot service
- return code
    - ok
    - error
- 尽量遵循pep8
- scribe日志格式
    - SCRIBE_CATEGORY='screenshot'
    - ``` scribe_msg = '\01'.join([str(ntime()),HOSTNAME,SCRIBE_CATEGORY,runtime,'0',source]) ```
-  依赖
    - 域名依赖
        - http://127.0.0.1/screenshot
    - 服务依赖
        - phantomjs 版本2.1.1
        - Python 版本 3.5.3  3.5.2 测试通过
        - redis 3.2.3  测试通过
    - 服务启动方式
        - ```/etc/init.d/redis start```
        - ``` python screenshot_daemon.py  start```
        - ``` python  /usr/bin/gunicorn -w 4 -b 0.0.0.0:80 screenshot_http:app ```
        



- 调用说明
    - 该服务约定根据url的md5值存放到路径
    -  ``` /data0/moosefs/client/screenshots/  + 前两位md5 + / + url md5 + .png```
    - ```save_pwd = SCREENSHOT_DIR + '/' + str(md5encode(url))[0:2] + '/' + str(md5encode(url)) + '.png'```
        - 请求参数说明,请求方式为post 格式为json 参数有两个
            - url "http://www.baidu.com"
            - cut  1000,560,0,0


 ``` width = cut.split(",")[0]  宽
        height= cut.split(",")[1] 高
        x = cut.split(",")[2] 起点x轴坐标
        y = cut.split(",")[3] 起点y轴坐标
 ```


    - 请求案例


```
curl -X POST \
  http://127.0.0.1/screenshot \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
        "lists": [
            {
                "url": "http://www.qq.com",
                "cut": "1000,560,0,0"
            },
            {
                "url": "http://www.baidu.com",
                "cut": "1920,1080,0,0"
            }         
        ]
}'
```


-  screenshot_flow  ![服务流程](http://7xnw62.com1.z0.glb.clouddn.com/screenshot_flow.png)


- cat /etc/supervisord.conf

> [unix_http_server]
file=/tmp/supervisor.sock   ; (the path to the socket file)
[supervisord]
logfile=/tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=100MB        ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10           ; (num of main logfile rotation backups;default 10)
loglevel=info                ; (log level;default info; others: debug,warn,trace)
pidfile=/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
nodaemon=false               ; (start in foreground if true;default false)
minfds=1024                  ; (min. avail startup file descriptors;default 1024)
minprocs=200                 ; (min. avail process descriptors;default 200)
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket
[program:screenshot]
command = gunicorn -w 4 -b 0.0.0.0:80 screenshot_http:app
directory=/opt/screenshots/
autostart=true
autorestart=true
startsecs=1
stderr_logfile=/opt/screenshots/logs/http_server.log
stdout_logfile=/opt/screenshots/logs/http_server.log



-------


##΢����screenshots˵����

- ΢������:  screenshots
- Python3 + Flask + Selenium + PhantomJS http screenshot service
- return code
    - ok
    - error
- ������ѭpep8
- scribe��־��ʽ
    - SCRIBE_CATEGORY='screenshot'
    - ``` scribe_msg = '\01'.join([str(ntime()),HOSTNAME,SCRIBE_CATEGORY,runtime,'0',source]) ```
-  ����
    - ��������
        - http://127.0.0.1/screenshot
    - ��������
        - phantomjs �汾2.1.1
        - Python �汾 3.5.3  3.5.2 ����ͨ��
        - redis 3.2.3  ����ͨ��
    - ����������ʽ
        - ```/etc/init.d/redis start```
        - ``` python screenshot_daemon.py  start```
        - ``` python  /usr/bin/gunicorn -w 4 -b 0.0.0.0:80 screenshot_http:app ```
        



- ����˵��
    - �÷���Լ������url��md5ֵ��ŵ�·��
    -  ``` /data0/moosefs/client/screenshots/  + ǰ��λmd5 + / + url md5 + .png```
    - ```save_pwd = SCREENSHOT_DIR + '/' + str(md5encode(url))[0:2] + '/' + str(md5encode(url)) + '.png'```
        - �������˵��,����ʽΪpost ��ʽΪjson ����������
            - url "http://www.baidu.com"
            - cut  1000,560,0,0


 ``` width = cut.split(",")[0]  ��
        height= cut.split(",")[1] ��
        x = cut.split(",")[2] ���x������
        y = cut.split(",")[3] ���y������
 ```


    - ������


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


-  screenshot_flow  ![��������](http://7xnw62.com1.z0.glb.clouddn.com/screenshot_flow.png)


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


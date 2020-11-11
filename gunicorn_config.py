# -*- coding: utf-8 -*-
"""
bind：IP地址
workers：启动进程数
worker_class: 工作模式.websocket需采取gevent：需依赖gevent包
loglevel：log日志等级
errorlog：log日志路径
daemon：是否后台运行
运行gunicorn命令： gunicorn NewPrinterBrain.wsgi -c gunicorn_config.py
"""

bind = "0.0.0.0:9000"
workers = 2
worker_class = 'gevent'
loglevel = 'error'
errorlog = "log_path/gunicorn_error.log"
accesslog = 'log_path/gunicorn.access.log'
daemon=True
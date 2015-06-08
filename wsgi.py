# coding: utf-8

import os

from wsgiref import simple_server
import leancloud

from app import app
from cloud import engine


APP_ID = os.environ.get('LC_APP_ID', 'vihmt0t5gk5p6x6hqdc8h8hybgyldlj8rkwh0kz177pxngyi')  # your app id
MASTER_KEY = os.environ.get('LC_APP_MASTER_KEY', '')  # your app master key

leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = simple_server.make_server('localhost', 8080, application)
    server.serve_forever()

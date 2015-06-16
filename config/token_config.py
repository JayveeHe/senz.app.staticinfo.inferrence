import json

__author__ = 'Jayvee'
import os

filedir = os.path.dirname(__file__)
token_config = json.loads(open('%s/config.json' % filedir, 'r').read())
# print token_config
LOGENTRIES_TOKEN = token_config['LOGENTRIES_TOKEN']
# ROLLBAR_TOKEN = ""
APP_ENV = token_config['APP_ENV']
LEANCLOUD_APP_ID = token_config['LEANCLOUD_APP_ID']
LEANCLOUD_APP_KEY = token_config['LEANCLOUD_APP_KEY']
LEANCLOUD_APP_MASTER_KEY = token_config['LEANCLOUD_APP_MASTER_KEY']
# -*- encoding:utf-8 -*-
import logging
import os
import sys
from analyzer.StaticInfoPredictor import staticinfo_predict
from analyzer import AppDict
from config import token_config
from package_leancloud_utils.leancloud_utils import LeancloudUtils
import logentries

__author__ = 'Jayvee'

from flask import Flask, request
import json

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
# TODO setup logentries
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logentries.LogentriesHandler(token_config.LOGENTRIES_TOKEN))
app = Flask(__name__)


@app.before_first_request
def initService():
    print token_config.APP_ENV
    logger.info('test')
    # pass


@app.route('/static_info/data', methods=['GET', 'POST'])
def get_applist_data():
    if request.method == 'GET':
        appdict = AppDict.AppDict()
        try:
            if 'limit' in request.args:
                dd = request.args['limit']
                limit_num = int(dd)
            else:
                limit_num = 100
            if 'label' in request.args:
                label = request.args['label']
            else:
                label = None
        except KeyError:
            # TODO setup logentries
            logger.info('keyerror')
            limit_num = 100  # default:limit_num=100
            label = None
        result_list = LeancloudUtils.get_remote_data(appdict, 'AppDict', limit_num, label)
        return json.dumps(result_list)
    # TODO add post method
    # TODO POST method for adding applist data
    return 'You Request Method is Not Correct!'


@app.route('/static_info/predict', methods=['POST'])
def predict_static_info():
    # params JSON validate
    req_data = {}
    try:
        req_data = json.loads(request.data)
    except ValueError, err_msg:
        # TODO setup logentries
        # logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        pass
    apps = req_data.get('app_list')

    if not apps:
        return '{"error":"param error:no app_list"}'
    # applist = apps.split(',')
    return json.dumps(staticinfo_predict(apps, True, True))


if __name__ == "__main__":
    app.debug = False
    app.run(port=8080)
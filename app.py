# -*- encoding:utf-8 -*-
import logging
import os
import sys
from analyzer.StaticInfoPredictor import staticinfo_predict
from analyzer import DataObject
from config import token_config
from package_leancloud_utils.leancloud_utils import LeancloudUtils
import logentries
from analyzer.MyExceptions import MsgException

__author__ = 'Jayvee'

from flask import Flask, request
import json

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
# TODO setup logentries
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lh = logentries.LogentriesHandler(token_config.LOGENTRIES_TOKEN)
format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
                           '%a %b %d %H:%M:%S %Y')
lh.setFormatter(format)
logger.addHandler(lh)
app = Flask(__name__)


@app.before_first_request
def initService():
    print token_config.APP_ENV
    logger.info('[%s]Service start' % token_config.LOG_TAG)
    # pass


@app.route('/static_info/data', methods=['GET', 'POST'])
def handle_applist_data():
    # get storage applist
    if request.method == 'GET':
        logger.info('[%s][handle_applist_data]receive get request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.args.keys()))
        appdict = DataObject.AppDict()
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
            logger.debug('[%s][handle_applist_data]keyerror' % token_config.LOG_TAG)
            limit_num = 100  # default:limit_num=100
            label = None
        result_list = LeancloudUtils.get_remote_data(appdict, 'AppDict', limit_num, label)
        return json.dumps(result_list)
    # TODO add post method
    # TODO POST method for adding applist data
    # push data to feedback
    if request.method == 'POST':
        logger.info('[%s][handle_applist_data]receive post request from %s' % (
            token_config.LOG_TAG, request.remote_addr))
        try:
            jsonobj = json.loads(request.data)
            DataObject.push_data_to_feedback(jsonobj)
        except ValueError, ve:
            logger.info('[%s][handle_applist_data]request data value error, details=%s, request_data=%s' % (
                token_config.LOG_TAG, ve, request.data))
            return '{"status": "failed", "msg": "request data value error"}'
        except KeyError, ke:
            logger.info('[%s][handle_applist_data]request data keyerror, details=%s, request_data=%s' % (
                token_config.LOG_TAG, ke, request.data))
            return '{"status": "failed", "msg": "request data keyerror"}'
        except MsgException, msg:
            logger.info('[%s][handle_applist_data]request data error, details=%s, request_data=%s' % (
                token_config.LOG_TAG, msg, request.data))
            return '{"status": "failed", "msg": "%s"}' % msg.message
        return '{"status": "success"}'
    return 'You Request Method is Not Correct!'


@app.route('/static_info/predict', methods=['POST'])
def predict_static_info():
    # params JSON validate
    req_data = {}
    try:
        logger.info('[%s][predict_static_info]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
    except ValueError, err_msg:
        # TODO setup logentries
        logger.debug('[%s][predict_static_info]%s' % (token_config.LOG_TAG, err_msg))
        # logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        # return json.dumps("{'status':'failed','msg':'%s'}" % err_msg)
    apps = req_data.get('app_list')

    if not apps:
        logger.debug('[%s][predict_static_info]post parameter error! params=%s' % (token_config.LOG_TAG, request.data))
        return '{"error":"param error:no app_list"}'
    return json.dumps(staticinfo_predict(apps, True, True))


if __name__ == "__main__":
    app.debug = False
    app.run(port=8080)
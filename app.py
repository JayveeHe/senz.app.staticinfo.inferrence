# -*- encoding:utf-8 -*-
import logging
import os
import sys
import time
import leancloud
from analyzer.StaticInfoPredictor import StaticInfoPredictor
from analyzer import DataObject
from analyzer import UserInfoManager
from config import token_config
from package_leancloud_utils.leancloud_utils import LeancloudUtils
import logentries
from analyzer.MyExceptions import MsgException

__author__ = 'Jayvee'

from flask import Flask, request
import json

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lh = logentries.LogentriesHandler(token_config.LOGENTRIES_TOKEN)
fm = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
                       '%a %b %d %H:%M:%S %Y')
lh.setFormatter(fm)
logger.addHandler(lh)
app = Flask(__name__)
predictor = StaticInfoPredictor()
predictor.staticinfo_predict([], is_local=False, is_degreed=True, add_binary=True)


@app.before_first_request
def initService():
    # print token_config.APP_ENV
    logger.info('[%s]Service start' % token_config.LOG_TAG)

    # pass


@app.route('/data', methods=['GET', 'POST'])
def handle_applist_data():
    # get storage applist
    if request.method == 'GET':
        logger.info('[%s][handle_applist_data]receive get request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.args.keys()))
        # appdict = DataObject.AppDict()
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
        result_list = LeancloudUtils.get_remote_data('app_dict', limit_num, label)
        return json.dumps(result_list)
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
            return '{"code": 103, "msg": "request data value error"}'
        except KeyError, ke:
            logger.info('[%s][handle_applist_data]request data keyerror, details=%s, request_data=%s' % (
                token_config.LOG_TAG, ke, request.data))
            return '{"code": 103, "msg": "request data keyerror"}'
        except MsgException, msg:
            logger.info('[%s][handle_applist_data]request data error, details=%s, request_data=%s' % (
                token_config.LOG_TAG, msg, request.data))
            return json.dumps({"code": 1, "msg": "%s" % msg.message})
        return json.dumps({"code": 0, "msg": "push data to feedback success, request_data= %s" % request.data})
    return 'You Request Method is Not Correct!'


@app.route('/predict', methods=['POST'])
def predict_static_info():
    # params JSON validate
    req_data = {}
    try:
        logger.info('[%s][predict_static_info]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.debug('[%s][predict_static_info]%s' % (token_config.LOG_TAG, err_msg))
        # logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        return json.dumps({'code': 103, 'msg': str(err_msg)})
    apps = req_data.get('applist')
    if not apps:
        logger.debug('[%s][predict_static_info]post parameter error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 1, 'msg': 'param error:no applist'})
    sim_dict = predictor.staticinfo_predict(apps, is_local=False, is_degreed=True, add_binary=True)
    return json.dumps(sim_dict)


@app.route('/log', methods=['POST'])
def log_userinfo():
    try:
        logger.info('[%s][log_userinfo]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
        userId = req_data['userId']
        timestamp = req_data['timestamp']
        staticInfo = req_data['staticInfo']
        UserInfoManager.push_userinfo(userId, staticInfo, timestamp)
        return json.dumps({'code': 0, 'msg': 'user %s staticinfo logged,timestamp=%s' % (userId, timestamp)})
    except MsgException, me:
        logger.debug('[%s][log_userinfo]POST log Error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 1, 'msg': str(me)})
    except ValueError, ve:
        logger.debug('[%s][log_userinfo]POST log Error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 103, 'msg': str(ve)})
    except Exception, e:
        logger.debug('[%s][log_userinfo]POST log Error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 1, 'msg': str(e)})


@app.route('/log/<userId>', methods=['GET'])
@app.route('/log/<userId>/', methods=['GET'])
def get_userinfo(userId):
    try:
        if userId:
            userinfo_list = UserInfoManager.query_userinfo_list(str(userId))
            return json.dumps({'code': 0, 'userinfo_list': userinfo_list})
        else:
            return json.dumps({'code': 103, 'msg': 'userId required'})
    except MsgException, me:
        logger.debug('[%s][log_userinfo]GET log Error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 1, 'msg': str(me)})


@app.route('/status', methods=['GET'])
def check_status():
    return 'The staticinfo.degree is running'


if __name__ == "__main__":
    app.debug = False
    app.run(port=8080)

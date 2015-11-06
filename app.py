# -*- encoding:utf-8 -*-
import logging
import os
import sys
from analyzer.staticInfo_predictor import StaticInfoPredictor
from analyzer import data_object
from analyzer import userinfo_manager
from config import token_config
from package_leancloud_utils.leancloud_utils import LeancloudUtils
import logentries
from analyzer.staticinfo_exceptions import MsgException

__author__ = 'Jayvee'

from flask import Flask, request, make_response
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

# Import bugsnag
import bugsnag
from bugsnag.flask import handle_exceptions

# Configure Bugsnag
bugsnag.configure(
    api_key=token_config.BUGSNAG_KEY,
    project_root=project_path,
)

# Attach Bugsnag to Flask's exception handler
handle_exceptions(app)

# init static info predictor
android_predictor = StaticInfoPredictor(platform='Android')
android_predictor.staticinfo_predict_platform([], add_nonbinary=True)
ios_predictor = StaticInfoPredictor(platform='iOS')
ios_predictor.staticinfo_predict_platform([], add_nonbinary=True)
predictor_dict = {'Android': android_predictor, 'iOS': ios_predictor}


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
            logger.error('[%s][handle_applist_data]keyerror' % token_config.LOG_TAG)
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
            data_object.push_data_to_feedback(jsonobj)
        except ValueError, ve:
            logger.error('[%s][handle_applist_data]request data value error, details=%s, request_data=%s' % (
                token_config.LOG_TAG, ve, request.data))
            resp = make_response('{"code": 103, "msg": "request data value error"}', 400)
            return resp
        except KeyError, ke:
            logger.error('[%s][handle_applist_data]request data keyerror, details=%s, request_data=%s' % (
                token_config.LOG_TAG, ke, request.data))
            resp = make_response('{"code": 103, "msg": "request data keyerror"}', 400)
            return resp
        except MsgException, msg:
            logger.error('[%s][handle_applist_data]request data error, details=%s, request_data=%s' % (
                token_config.LOG_TAG, msg, request.data))
            resp = make_response(json.dumps({"code": 1, "msg": "%s" % msg.message}), 400)
            return resp
        return json.dumps({"code": 0, "msg": "push data to feedback success, request_data= %s" % request.data})
    return 'You Request Method is Not Correct!'


@app.route('/predict', methods=['POST'])
def predict_static_info():
    # params JSON validate
    # req_data = {}
    try:
        logger.info('[%s][predict_static_info]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.error('[%s][predict_static_info]%s' % (token_config.LOG_TAG, err_msg))
        # logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        resp = make_response(json.dumps({'code': 103, 'msg': str(err_msg)}), 400)
        return resp
    apps = req_data.get('applist')
    if not apps:
        logger.error('[%s][predict_static_info]post parameter error! params=%s' % (token_config.LOG_TAG, request.data))
        resp = make_response(json.dumps({'code': 1, 'msg': 'param error:no applist'}), 400)
        return resp
    sim_dict = android_predictor.staticinfo_predict(apps, is_local=False, is_degreed=True, add_nonbinary=True)
    # transform the prob
    # for key in sim_dict.keys():
    #     if '-' in key:
    #         levels = key.split('-')
    #         first_level = levels[0]
    #         second_level = levels[1]
    #         if first_level in sim_dict.keys():
    #             sim_dict[first_level][second_level] = sim_dict[key]
    #         else:
    #             sim_dict[first_level] = {second_level: sim_dict[key]}
    #         del sim_dict[key]
    logger.info('[%s][predict_static_info]%s\'s request success, sim dic =%s' % (
        token_config.LOG_TAG, request.remote_addr, json.dumps(sim_dict)))
    return json.dumps(sim_dict)


@app.route('/predict_level', methods=['POST'])
def predict_static_info_level():
    # params JSON validate
    # req_data = {}
    try:
        logger.info('[%s][predict_static_info_level]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.error('[%s][predict_static_info]%s' % (token_config.LOG_TAG, err_msg))
        # logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        resp = make_response(json.dumps({'code': 103, 'msg': str(err_msg)}), 400)
        return resp
    apps = req_data.get('applist')
    if not apps:
        logger.error('[%s][predict_static_info]post parameter error! params=%s' % (token_config.LOG_TAG, request.data))
        resp = make_response(json.dumps({'code': 1, 'msg': 'param error:no applist'}), 400)
        return resp
    sim_dict = android_predictor.staticinfo_predict(apps, is_local=False, is_degreed=True, add_nonbinary=True)
    # transform the prob
    for key in sim_dict.keys():
        if '-' in key:
            levels = key.split('-')
            first_level = levels[0]
            second_level = levels[1]
            if first_level in sim_dict.keys():
                sim_dict[first_level][second_level] = sim_dict[key]
            else:
                sim_dict[first_level] = {second_level: sim_dict[key]}
            del sim_dict[key]
    logger.info('[%s][predict_static_info]%s\'s request success, sim dic =%s' % (
        token_config.LOG_TAG, request.remote_addr, json.dumps(sim_dict)))
    return json.dumps(sim_dict)


@app.route('/predict_platform', methods=['POST'])
def predict_static_info_platform():
    try:
        logger.info('[%s][predict_static_info_platform]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
        apps = req_data['applist']
        platform = req_data['platform']
        predictor = predictor_dict[platform]
        sim_dict = predictor. \
            staticinfo_predict_platform(apps, add_nonbinary=True)  # transform the prob
        for key in sim_dict.keys():
            if '-' in key:
                levels = key.split('-')
                first_level = levels[0]
                second_level = levels[1]
                if first_level in sim_dict.keys():
                    sim_dict[first_level][second_level] = sim_dict[key]
                else:
                    sim_dict[first_level] = {second_level: sim_dict[key]}
                del sim_dict[key]
        logger.info('[%s][predict_static_info_platform]%s\'s request success, sim dic =%s' % (
            token_config.LOG_TAG, request.remote_addr, json.dumps(sim_dict)))
        return json.dumps(sim_dict)

    except ValueError, err_msg:
        logger.error('[%s][predict_static_info]%s' % (token_config.LOG_TAG, err_msg))
        # logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        resp = make_response(json.dumps({'code': 103, 'msg': str(err_msg)}), 400)
        return resp
    except KeyError, keyerr:
        logger.error(
            '[%s][predict_static_info_platform]post parameter error! params=%s' % (token_config.LOG_TAG, request.data))
        resp = make_response(json.dumps({'code': 1, 'msg': 'key error:%s' % keyerr}), 400)
        return resp


@app.route('/log', methods=['POST'])
def log_userinfo():
    try:
        logger.info('[%s][log_userinfo]receive post request from %s, param data=%s' % (
            token_config.LOG_TAG, request.remote_addr, request.data))
        req_data = json.loads(request.data)
        userId = req_data['userId']
        timestamp = req_data['timestamp']
        applist = req_data['applist']
        userRawdataId = req_data['userRawdataId']
        staticInfo = android_predictor.staticinfo_predict(applist, add_nonbinary=True)
        userinfo_manager.push_userinfo(userId, applist, staticInfo, timestamp, userRawdataId)
        return json.dumps({'code': 0, 'msg': 'user %s staticinfo logged,timestamp=%s' % (userId, timestamp)})
    except MsgException, me:
        logger.error(
            '[%s][log_userinfo]POST log Error! detail = %s\n params=%s' % (token_config.LOG_TAG, me, request.data))
        resp = make_response(json.dumps({'code': 1, 'msg': str(me)}), 400)
        return resp
    except ValueError, ve:
        logger.error(
            '[%s][log_userinfo]POST log ValueError! detail = %s\n params=%s' % (token_config.LOG_TAG, ve, request.data))
        resp = make_response(json.dumps({'code': 103, 'msg': str(ve)}), 400)
        return resp
    except KeyError, ke:
        logger.error('[%s][log_userinfo]POST log KeyError key=%s params=%s'
                     % (token_config.LOG_TAG, ke, request.data))
        resp = make_response(json.dumps({'code': 103, 'msg': 'KeyError,Key=%s' % ke}), 400)
        return resp
    except Exception, e:
        logger.error('[%s][log_userinfo]POST log Unknown Error!detail = %s\n params=%s' % (
            token_config.LOG_TAG, e, request.data))
        resp = make_response(json.dumps({'code': 1, 'msg': str(e)}), 400)
        return resp


@app.route('/log/<userId>', methods=['GET'])
@app.route('/log/<userId>/', methods=['GET'])
def get_userinfo(userId):
    try:
        if userId:
            userinfo_list = userinfo_manager.query_userinfo_list(str(userId))
            return json.dumps({'code': 0, 'userinfo_list': userinfo_list})
        else:
            return json.dumps({'code': 103, 'msg': 'userId required'})
    except MsgException, me:
        logger.error('[%s][log_userinfo]GET log Error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 1, 'msg': str(me)})
    except Exception, e:
        logger.error('[%s][log_userinfo]GET log Error! params=%s' % (token_config.LOG_TAG, request.data))
        return json.dumps({'code': 1, 'msg': e.message})


@app.route('/status', methods=['GET'])
def check_status():
    return 'The staticinfo.degree is running'


if __name__ == "__main__":
    app.debug = False
    app.run(port=8080)

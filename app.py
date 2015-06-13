# -*- encoding:utf-8 -*-
import logging
from analyzer.StaticInfoPredictor import staticinfo_predict
from analyzer import AppDict
from leancloud_utils.LeancloudUtils import LeancloudUtils


__author__ = 'Jayvee'

from flask import Flask, request
import json

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/static_info/data', methods=['GET'])
def get_static_info_python():
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
            logger.info('keyerror')
            limit_num = 100  # default:limit_num=100
            label = None
        result_list = LeancloudUtils.get_remote_data(appdict, 'AppDict', limit_num, label)
        return json.dumps(result_list)
    return 'You Request Method is Not Correct!'


@app.route('/static_info/predict', methods=['POST'])
def get_static_info_by_applist():
    if request.method == 'POST':
        # params JSON validate
        req_data = {}
        try:
            req_data = json.loads(request.data)
        except ValueError, err_msg:
            logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        apps = req_data.get('app_list')

        if not apps:
            return '{"error":"param error:no app_list"}'
        # applist = apps.split(',')
        return json.dumps(staticinfo_predict(apps, True, True))
    return 'You Request Method is Not Correct!'


if __name__ == "__main__":
    app.debug = False
    app.run(port=8080)
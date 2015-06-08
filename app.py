# -*- encoding:utf-8 -*-
import logging
from analyzer.StaticInfoPredictor import staticinfo_predict

from leancloud_utils import settings
from analyzer import AppDict
from leancloud_utils.LeancloudUtils import LeancloudUtils


__author__ = 'zhongziyuan', 'Jayvee'

from flask import Flask, request
import json

logger = logging.getLogger(__name__)
app = Flask(__name__)



@app.route('/static_info_data', methods=['GET'])
def get_static_info_python():
    if request.method == 'GET':
        # lcu = LeancloudUtils(settings.APP_ID, settings.APP_KEY)
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


@app.route('/static_info_predict', methods=['GET'])
def get_static_info_by_applist():
    if request.method == 'GET':
        # lcu = LeancloudUtils(settings.APP_ID, settings.APP_KEY)
        # appdict = AppDict.AppDict()
        apps = request.args.get('app_list')
        if not apps:
            return '{"error":"param error:no app_list"}'
        applist = apps.split(',')
        return json.dumps(staticinfo_predict(applist, True, True))
        # return json.dumps(i.get_labels(apps.split(',')))
    # result_list = LeancloudUtils.get_remote_data(appdict, 'AppDict', limit_num, label)
    # return json.dumps(result_list)
    return 'You Request Method is Not Correct!'


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
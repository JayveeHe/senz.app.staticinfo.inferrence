import json
import logging
import os
import math
from analyzer.AppDict import AppDict
from package_leancloud_utils.leancloud_utils import LeancloudUtils

__author__ = 'Jayvee'

file_path = os.path.dirname(os.path.abspath(__file__))
# print file_path
logger = logging.getLogger(__name__)


def get_applist_local():
    try:
        fin = open('%s/data/appdict.json' % file_path, 'r')
        jsonstr = fin.read()
        jsonobj = json.loads(jsonstr)
        return jsonobj
    except IOError:
        logger.info('ioerror!')


def get_applist_remote(label=None):
    appdict = AppDict()
    return LeancloudUtils.get_remote_data(appdict, 'AppDict', 2000, label)


def build_app_dict(is_local=True):
    try:
        if is_local:
            jsonobj = get_applist_local()
        else:
            jsonobj = get_applist_remote()
        app_dict = {}
        for obj in jsonobj:
            if obj['app'] in app_dict:
                app_dict[obj['app']][obj['label']] = obj['degree']
            else:
                app_dict[obj['app']] = {obj['label']: obj['degree']}
        return app_dict
    except IOError:
        logger.info('ioerror!')


def build_label_dict(is_local=True, label=None):
    try:
        if is_local:
            jsonobj = get_applist_local()
        else:
            jsonobj = get_applist_remote(label)
        label_dict = {}
        for obj in jsonobj:
            if obj['label'] in label_dict:
                label_dict[obj['label']][obj['app']] = obj['degree']
            else:
                label_dict[obj['label']] = {obj['app']: obj['degree']}
        return label_dict
    except IOError:
        logger.info('ioerror!')


def staticinfo_predict(user_applist, is_local=False, is_degreed=True):
    apps_dict = build_app_dict(is_local)
    labels_dict = build_label_dict(is_local)
    labels = []
    vecinfo = {}
    # get user's labels and appvec
    for user_app in user_applist:
        if user_app in apps_dict:
            for label in apps_dict[user_app].keys():
                if label not in labels:
                    labels.append(label)
                    vecinfo[label] = {user_app: apps_dict[user_app][label]}
                else:
                    vecinfo[label][user_app] = apps_dict[user_app][label]
    # build user's vec
    sim_dict = {}
    for label in labels:
        user_vec = []
        model_vec = []
        for model_app_key in labels_dict[label].keys():
            if is_degreed:
                degree = labels_dict[label][model_app_key]
            else:
                degree = 1
            if degree > 0:
                weight = 1
            else:
                weight = 1
            model_vec.append((weight, degree))
            if model_app_key in user_applist:
                user_vec.append((weight, degree))
            else:
                user_vec.append((0, 0))
        sim_dict[label] = cal_cos_dist(user_vec, model_vec)
    return sim_dict


def cal_cos_dist(vec1=[()], vec2=[()]):
    if len(vec1) != len(vec2) or not (isinstance(vec1, list) and isinstance(vec2, list)):
        logger.info('inputs are not list with same length!')
        return None
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(len(vec1)):
        numerator += math.fabs(vec1[i][1]) * vec2[i][1] * vec1[i][0] * vec2[i][0]
        denominator1 += vec1[i][1] ** 2 * vec1[i][0] ** 2
        denominator2 += vec2[i][1] ** 2 * vec2[i][0] ** 2
    sim = numerator / math.sqrt(denominator1 * denominator2 + 0.0001)
    return sim


"""
if __name__ == '__main__':
    print staticinfo_predict(
        ["com.kplus.car", "cn.buding.martin", 'com.ubercab.driver', 'com.aibang.abbus.bus', 'com.didapinche.booking',
         'cn.edaijia.android.client', 'com.bkl.activity',
         'com.yicai.news',
         'cn.com.sina.finance'],
        is_local=True, is_degreed=False)
    print staticinfo_predict(
        ["com.kplus.car", "cn.buding.martin", 'com.ubercab.driver', 'com.aibang.abbus.bus', 'com.didapinche.booking',
         'cn.edaijia.android.client', 'com.bkl.activity',
         'com.yicai.news',
         'cn.com.sina.finance'],
        is_local=True, is_degreed=True)
    print staticinfo_predict(
        ['com.ubercab.driver', "cn.buding.martin",
         'com.bkl.activity',

         'cn.com.sina.finance'],
        is_local=True, is_degreed=True)
    print staticinfo_predict(
        ["cn.buding.martin", "cn.com.tiros.android.navidog", "com.sdu.didi.gui", "com.mapbar.android.trybuynavi",
         'com.bkl.activity', "com.ourlinc", "com.ubercab.driver", "com.mapbar.android.trybuynavi",
         "com.autohome.mycar", 'com.sdu.didi.psnger',
         'cn.com.sina.finance'],
        is_local=True, is_degreed=True)
    print staticinfo_predict(
        ["cn.buding.martin", "com.mygolbs.mybus", "com.sdu.didi.psnger", "com.edcsc.wbus", "cn.chinabus.main",
         'cn.com.sina.finance'],
        is_local=True, is_degreed=True)
    print staticinfo_predict(
        ["cn.buding.martin", "com.mygolbs.mybus", "com.sdu.didi.psnger", "com.edcsc.wbus", "cn.chinabus.main",
         'cn.com.sina.finance'],
        is_local=True, is_degreed=False)
"""
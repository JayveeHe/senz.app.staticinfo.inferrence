import copy
import json
import os
import math
# from app import logger
from package_leancloud_utils.leancloud_utils import LeancloudUtils

__author__ = 'Jayvee'

file_path = os.path.dirname(os.path.abspath(__file__))
# print file_path


class StaticInfoPredictor():
    def __init__(self):
        self.inst_applist = []
        self.inst_app_dict = {}
        self.inst_label_dict = {}

    @staticmethod
    def get_applist_local():
        """
        get applist by local json file
        """
        try:
            fin = open('%s/data/appdict.json' % file_path, 'r')
            jsonstr = fin.read()
            jsonobj = json.loads(jsonstr)
            return jsonobj
        except IOError:
            # logger.info('ioerror!')
            print 'get_applist_local ioerror!'

    @staticmethod
    def get_applist_remote(label=None):
        """
        get applist by leancloud storage
        """
        # REMOTE_DB_APP_ID = '3plka1gwb9mlayuguyh792dqajtpsa05nu77om9v8twr86ly'
        # REMOTE_DB_APP_KEY = 'a843jsdl0r49fqta11nl4ypm4l77shqk8vqag5bvfytzfsrd'
        # leancloud.init(REMOTE_DB_APP_ID, REMOTE_DB_APP_KEY)
        # remote_app_dict = leancloud.Object.extend('app_dict')
        # remote_query = leancloud.Query(remote_app_dict)
        # appdict = _find(remote_query)
        # # appdict = AppDict()
        # applist_result = []
        # for item in appdict:
        #     applist_result.append(item.attributes)
        applist_result = LeancloudUtils.get_remote_data('app_dict')
        return applist_result

    @staticmethod
    def get_notbinary_applist_remote():
        """
        get not binary applist by leancloud storage
        :return:
        """
        notbi_applist_result = LeancloudUtils.get_remote_data('app_dict_not_binary')
        # process not binary degree
        result = []
        for item in notbi_applist_result:
            label = item['label']
            app = item['app']
            for degree_label in item['degree'].keys():
                degree = item['degree'][degree_label]
                if degree != 0:
                    result.append(
                        {'app': app,
                         'label': '%s-%s' % (label, degree_label),
                         'degree': degree})
        return result

    @staticmethod
    def _find(query):
        # fetch all data from leancloud
        result = []
        count = query.count()
        pages = count / 1000 + 1
        # print count
        for i in range(pages):
            _query = copy.deepcopy(query)
            _query.limit(1000)
            _query.skip(i * 1000)
            res = _query.find()
            for item in res:
                result.append(item)
        return result

    @staticmethod
    def build_app_dict(is_local=True, add_binary=False):
        """
        build app dict(appname as key, labels of this app as values)
        """
        try:
            if is_local:
                jsonobj = StaticInfoPredictor.get_applist_local()
            else:
                jsonobj = StaticInfoPredictor.get_applist_remote()
                if add_binary:
                    jsonobj.extend(StaticInfoPredictor.get_notbinary_applist_remote())
            app_dict = {}
            for obj in jsonobj:
                if obj['app'] in app_dict:
                    app_dict[obj['app']][obj['label']] = obj['degree']
                else:
                    app_dict[obj['app']] = {obj['label']: obj['degree']}
            return app_dict
        except IOError:
            # logger.debug('build_app_dict ioerror!')
            print 'build_app_dict ioerror!'

    @staticmethod
    def build_label_dict(is_local=True, label=None, add_binary=False):
        """
        build label dict(label as key, applist that has the label as values)
        """
        try:
            if is_local:
                jsonobj = StaticInfoPredictor.get_applist_local()
            else:
                jsonobj = StaticInfoPredictor.get_applist_remote(label)
                if add_binary:
                    jsonobj.extend(StaticInfoPredictor.get_notbinary_applist_remote())
            label_dict = {}
            for obj in jsonobj:
                if obj['label'] in label_dict:
                    label_dict[obj['label']][obj['app']] = obj['degree']
                else:
                    label_dict[obj['label']] = {obj['app']: obj['degree']}
            return label_dict
        except IOError:
            # logger.debug('build_label_dict ioerror!')
            print 'build_label_dict ioerror!'

    @staticmethod
    def build_label_apps_dict(applist):
        try:
            app_dict = {}
            label_dict = {}
            for obj in applist:
                if obj['app'] in app_dict:
                    app_dict[obj['app']][obj['label']] = obj['degree']
                else:
                    app_dict[obj['app']] = {obj['label']: obj['degree']}
                if obj['label'] in label_dict:
                    label_dict[obj['label']][obj['app']] = obj['degree']
                else:
                    label_dict[obj['label']] = {obj['app']: obj['degree']}
            return app_dict, label_dict
        except IOError:
            # logger.debug('build_label_apps_dict ioerror!')
            print 'build_label_apps_dict ioerror!'

    def staticinfo_predict(self, user_applist, is_local=False, is_degreed=True, add_binary=False):
        """
        predict a user's potential interest labels by applist
        """
        if len(self.inst_applist) == 0:
            if is_local:
                self.inst_applist = StaticInfoPredictor.get_applist_local()
            else:
                self.inst_applist = StaticInfoPredictor.get_applist_remote()
                if add_binary:
                    self.inst_applist.extend(StaticInfoPredictor.get_notbinary_applist_remote())
            dicts = StaticInfoPredictor.build_label_apps_dict(self.inst_applist)
            self.inst_app_dict = dicts[0]
            self.inst_label_dict = dicts[1]
        apps_dict = self.inst_app_dict
        labels_dict = self.inst_label_dict
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
    """
    calculate cosine distance
    """
    if len(vec1) != len(vec2) or not (isinstance(vec1, list) and isinstance(vec2, list)):
        # logger.info('inputs are not list with same length!')
        print 'cal_cos_dist inputs are not list with same lenght!'
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


if __name__ == '__main__':
    # sdas = LeancloudUtils.get_remote_data('app_dict',max_num=1030)
    # notbi = LeancloudUtils.get_remote_data('app_dict_not_binary')
    # notbi = get_notbinary_applist_remote()
    # print notbi[0]
    pass
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

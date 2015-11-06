# coding=utf-8
import copy
import os
import math

import leancloud

from analyzer import data_object
from config import token_config

__author__ = 'Jayvee'

leancloud.init(token_config.LEANCLOUD_APP_ID, token_config.LEANCLOUD_APP_KEY)


class LeancloudUtils():
    def __init__(self):
        # app_dict = AppDict.AppDict()# 提前定义
        pass

    app_dict = data_object.AppDict()  # 提前定义

    @staticmethod
    def get_remote_data(tablename, max_num=None, label=None):
        """
        generally get remote data from leancloud
        :param tablename: name of the table to be queried
        :param max_num: max count of the result
        :return: list of result.
        """
        # REMOTE_DB_APP_ID = '3plka1gwb9mlayuguyh792dqajtpsa05nu77om9v8twr86ly'
        # REMOTE_DB_APP_KEY = 'a843jsdl0r49fqta11nl4ypm4l77shqk8vqag5bvfytzfsrd'
        # leancloud.init(REMOTE_DB_APP_ID, REMOTE_DB_APP_KEY)
        leancloud.init(token_config.LEANCLOUD_APP_ID, token_config.LEANCLOUD_APP_KEY)
        objclass = leancloud.Object.extend(tablename)
        query = leancloud.Query(objclass)
        # max_page_num = int(math.ceil(max_num / 1000.0))
        # result_list = []
        # if max_num > 1000:
        #     num_per_page = 1000
        # else:
        #     num_per_page = max_num
        # for i in range(max_page_num):
        #     # when there is more than 1000 items in query,use [skip] to reach all result
        #     if label is None:
        #         result = query.do_cloud_query('select * from %s limit ?,?' % tablename, i * 1000, num_per_page)
        #     else:
        #         result = query.do_cloud_query('select * from %s where label=? limit ?,?' % (tablename), label,
        #                                       i * 1000, num_per_page)
        #     results = result.results
        #     for app_single in results:
        #         result_list.append(app_single.attributes)
        if label:
            query.equal_to('label', label)
        if max_num is not None:
            query.limit(max_num if max_num < 1000 else 1000)
        result_list = []
        try:
            query_list = LeancloudUtils._find(query, max_num)
            for item in query_list:
                result_list.append(item.attributes)
        except leancloud.errors.LeanCloudError, lce:
            print lce
        return result_list

    @staticmethod
    def _find(query, max_num=None):
        # fetch data from leancloud
        result = []
        if max_num is not None and max_num < 1000:
            return query.find()
        count = query.count()
        pages = count / 1000 + 1
        # print count
        query_count = 0
        for i in range(pages):
            _query = copy.deepcopy(query)
            _query.limit(1000)
            _query.skip(i * 1000)
            res = _query.find()
            for item in res:
                if max_num and query_count >= max_num:
                    return result
                result.append(item)
                query_count += 1
        return result


'''
    @staticmethod
    def get_label(apps):
        if not isinstance(apps, list):
            print 'Input data must be list !'
            return {}
        result_dict = {}
        query = leancloud.Query(LeancloudUtils.app_dict)
        query.do_cloud_query('')
'''

# 测试demo
if __name__ == '__main__':
    # lcu = LeancloudUtils(settings.APP_ID, settings.APP_KEY)
    appdict = data_object.AppDict()
    appdict_result = LeancloudUtils.get_remote_data(appdict, 'AppDict', 2000)
    # tests output
    import sys
    import json

    try:
        file_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:  # We are the main py2exe script, not a module
        file_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    fout = open('appdict.json', 'w')
    fout.write(json.dumps(appdict_result))

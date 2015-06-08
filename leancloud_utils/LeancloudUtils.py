# coding=utf-8
import os
import math

import leancloud

from leancloud_utils import settings
from analyzer import AppDict


__author__ = 'Jayvee'

leancloud.init(settings.APP_ID, settings.APP_KEY)


class LeancloudUtils():
    def __init__(self):
        # app_dict = AppDict.AppDict()# 提前定义
        pass

    app_dict = AppDict.AppDict()  # 提前定义

    @staticmethod
    def get_remote_data(objclass, tablename, max_num, label=None):
        """
        generally get remote data from leancloud
        :param objclass: class instance to be queried, Extends from Leancloud.Object
        :param tablename: name of the table to be queried
        :param max_num: max count of the result
        :return: list of result.
        """
        query = leancloud.Query(objclass)
        max_page_num = int(math.ceil(max_num / 1000.0))
        result_list = []
        if max_num > 1000:
            num_per_page = 1000
        else:
            num_per_page = max_num
        for i in range(max_page_num):
            # when there is more than 1000 items in query,use [skip] to reach all result
            if label is None:
                result = query.do_cloud_query('select * from %s limit ?,?' % tablename, i * 1000, num_per_page)
            else:
                result = query.do_cloud_query('select * from %s where label=? limit ?,?' % (tablename), label,
                                              i * 1000, num_per_page)
            results = result.results
            for app_single in results:
                result_list.append(app_single.attributes)
        return result_list


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
    appdict = AppDict.AppDict()
    appdict_result = LeancloudUtils.get_remote_data(appdict, 'AppDict', 2000)
    # test output
    import sys
    import json

    try:
        file_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:  # We are the main py2exe script, not a module
        file_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    fout = open('appdict.json', 'w')
    fout.write(json.dumps(appdict_result))


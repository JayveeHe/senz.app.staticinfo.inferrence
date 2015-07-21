import json
import unittest
from app import app

__author__ = 'Jayvee'


class MyUserLogTest(unittest.TestCase):
    def setUp(self):
        super(MyUserLogTest, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        super(MyUserLogTest, self).tearDown()
        app.config['TESTING'] = False

    def test_staticinfo_log(self):
        req_data = json.dumps({
            "applist": ["com.runtastic.android.sixpack.lite",
                        "com.inisoft.mediaplayer.a",
                        "com.tencent.mm",
                        "com.UCMobile",
                        "com.icbc",
                        "com.quora.android",
                        "com.twitter.android",
                        "com.tencent.mobileqq",
                        "com.zishell.javatest",
                        "flipboard.app",
                        "com.netease.newsreader.activity",
                        "cn.etouch.ecalendar",
                        "com.netease.cloudmusic",
                        "com.google.android.apps.translate",
                        "de.blinkt.mashang6",
                        "com.google.android.apps.plus",
                        "com.google.android.play.games",
                        "com.speedsoftware.rootexplorer",
                        "com.sina.weibo",
                        "com.alicall.androidzb",
                        "fq.router2",
                        "com.google.android.youtube",
                        "com.android.chrome",
                        "jp.ne.kutu.Panecal",
                        "com.baidu.input",
                        "com.qihoo.yunpan",
                        "com.kumobius.android.duet"],
            "userId": "558a5ee7e4b0acec6b941e96",
            "timestamp": 1437238667744,
            "userRawdataId": "just for test"
        })
        rv = self.app.post('/log', data=req_data)
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(0, result['code'])

        # def test_staticinfo_invalid_log(self):
        #     req_data = json.dumps({
        #         "applist": ["com.runtastic.android.sixpack.lite",
        #                     "com.inisoft.mediaplayer.a",
        #                     "com.tencent.mm",
        #                     "com.UCMobile",
        #                     "com.icbc",
        #                     "com.quora.android",
        #                     "com.twitter.android",
        #                     "com.tencent.mobileqq",
        #                     "com.zishell.javatest",
        #                     "flipboard.app",
        #                     "com.netease.newsreader.activity",
        #                     "cn.etouch.ecalendar",
        #                     "com.netease.cloudmusic",
        #                     "com.google.android.apps.translate",
        #                     "de.blinkt.mashang6",
        #                     "com.google.android.apps.plus",
        #                     "com.google.android.play.games",
        #                     "com.speedsoftware.rootexplorer",
        #                     "com.sina.weibo",
        #                     "com.alicall.androidzb",
        #                     "fq.router2",
        #                     "com.google.android.youtube",
        #                     "com.android.chrome",
        #                     "jp.ne.kutu.Panecal",
        #                     "com.baidu.input",
        #                     "com.qihoo.yunpan",
        #                     "com.kumobius.android.duet"],
        #         "userId": "558a5ee7e4b0acec6b941e96",
        #         "timestamp": 1437238667744,
        #         "userRawdataId": "just for test"
        #     })
        #     rv = self.app.post('/log', data=req_data)
        #     self.assertEqual(200, rv.status_code)
        #     result = json.loads(rv.data)
        #     self.assertEqual(0, result['code'])

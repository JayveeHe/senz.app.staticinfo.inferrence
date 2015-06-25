# coding:utf8
import json
import unittest
from app import app

__author__ = 'Jayvee'


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        super(TestFlaskApp, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        super(TestFlaskApp, self).tearDown()
        app.config['TESTING'] = False

    def test_get_applist_data(self):
        rv = self.app.get('/static_info/data')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(100, len(result))

    def test_get_applist_data_limit(self):
        rv = self.app.get('/static_info/data?limit=920')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(920, len(result))
        rv = self.app.get('/static_info/data?limit=20')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(20, len(result))
        rv = self.app.get('/static_info/data?limit=0')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(0, len(result))

    def test_get_applist_data_label(self):
        rv = self.app.get('/static_info/data?label=has_car')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('has_car', result[0]['label'])
        rv = self.app.get('/static_info/data?label=sports_news')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('sports_news', result[0]['label'])

    def test_get_applist_data_invalidlabel(self):
        rv = self.app.get('/static_info/data?label=haha')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(0, len(result))

    def test_get_applist_data_label_limit(self):
        rv = self.app.get('/static_info/data?label=has_car&limit=11')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('has_car', result[0]['label'])
        self.assertEqual(11, len(result))

    def test_predict_static_info_invalidparams(self):
        rv = self.app.post('/static_info/predict', data='')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('param error:no app_list', result['error'])
        rv = self.app.post('/static_info/predict', data='dadfasdfasdf')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('param error:no app_list', result['error'])
        rv = self.app.post('/static_info/predict', data='{}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('param error:no app_list', result['error'])

    def test_predict_static_info(self):
        rv = self.app.post('/static_info/predict', data='{"app_list": ["com.yidian.nba","com.dota.emu"]}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('gender', result.keys()[0])
        # !!!! this value maybe changed when new data is pushed to the database!!!
        self.assertEqual(0.193666930476603, result['gender'])

    def test_push_feedback_data(self):
        rv = self.app.post('/static_info/data',
                           data='{"labels":["has_car","study"],"applist":["test1","test2","serser"]}')
        self.assertEqual(200, rv.status_code)
        strjson = rv.data
        result = json.loads(strjson)
        self.assertEqual('success', result['status'])

    def test_push_feedback_invaliddata(self):
        # test invalid data
        rv = self.app.post('/static_info/data', data='{}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('failed', result['status'])
        self.assertEqual('request data keyerror', result['msg'])
        # test empty data or keyerror
        rv = self.app.post('/static_info/data', data='{}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('failed', result['status'])
        # test invalid type of labels
        rv = self.app.post('/static_info/data', data='{"labels":123123,"applist":["asdfad","adseew"]}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('failed', result['status'])
        self.assertEqual('labels should be a list!', result['msg'])
        # test invalid type of applist
        rv = self.app.post('/static_info/data', data='{"labels":["has_car","study"],"applist":"123se"}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('failed', result['status'])
        self.assertEqual('applist should be a list!', result['msg'])
        # test empty labels
        rv = self.app.post('/static_info/data', data='{"labels":[],"applist":["asdfad","adseew"]}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('failed', result['status'])
        # test empty applist
        rv = self.app.post('/static_info/data', data='{"labels":["study"],"applist":[]}')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual('failed', result['status'])